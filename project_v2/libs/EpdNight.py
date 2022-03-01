from datetime import datetime
from PyQt5.QtCore import QThread
from PyQt5 import QtCore
# import time

from contants.path_constants import (
    dir_log,
    dir_armkbr,
    dir_archive,
    arm_buf,
    unb64_rabis,
    trans_disk,
    puds_disk,
    CLI,
)

from libs.FileExplorer import FileExplorer


class NightCicle(QThread):

    log_str = QtCore.pyqtSignal(str, bool, bool)

    def __init__(self,form):
        QThread.__init__(self)
        self.work = True
        self.file_explorer = FileExplorer()
        self.file_explorer.log_str.connect(form.log)

    def run(self):
        while self.work:
            time_now = datetime.time(datetime.now())
            time_to = datetime.time(datetime.strptime("09:00:00","%H:%M:%S"))
            time_from = datetime.time(datetime.strptime("20:30:00","%H:%M:%S"))
            # C 20:30 до 9 00 
            if time_to < time_now and time_now > time_from:
                self.file_explorer.check_dir(dir_log)
                self.file_explorer.check_dir(dir_armkbr + "\\exg\\rcv")

                current_date = datetime.now().strftime("%d.%m.%Y")

                if self.file_explorer.count_files_in_folder(dir_armkbr + "\\exg\\rcv") == 0:
                    self.log_str.emit("Нет файлов к отправке!", False, False)

                else:
                    self.file_explorer.check_dir(dir_archive)
                    self.file_explorer.check_dir(arm_buf)

                    self.file_explorer.move_files(dir_armkbr + "\\exg\\rcv", arm_buf)

                    # self.file_explorer.move_files() Исключить квитки без расширения

                    self.file_explorer.decode_files(unb64_rabis, arm_buf, dir_log)

                    arc_dir = dir_archive + "\\" + current_date + "\\uarm3\\inc\\ed"

                    self.file_explorer.check_dir(arc_dir)

                    self.file_explorer.copy_files(arm_buf, arc_dir, r".*\.ed\.xml$", name_of_doc='.ed.xml')
                    self.file_explorer.copy_files(arm_buf, arc_dir, r".*ed211.*\.ed\.xml$", name_of_doc='e211.ed.xml')

                    trans_disk_path = trans_disk + "IN_OEBS_BIK\\044525000"

                    self.file_explorer.copy_files(arm_buf, trans_disk_path, r".*\.ed\.xml$", name_of_doc='.ed.xml')
                    self.file_explorer.copy_files(
                        arm_buf, trans_disk_path, r".*ed211.*\.ed\.xml$", name_of_doc='ed211.ed.xml'
                    )

                    self.file_explorer.copy_files(arm_buf, puds_disk + "input", r".*\.ed$", name_of_doc='.ed')
                    self.file_explorer.copy_files(
                        arm_buf, puds_disk + "input", r".*ed211.*\.eds", name_of_doc='.ed211.eds'
                    )

                    self.file_explorer.delete_files(arm_buf, r".*\.xml$", name_of_doc='.xml')

                    self.file_explorer.copy_files(arm_buf, dir_armkbr + "\\exg\\rcv\\1")

                    self.file_explorer.delete_files(arm_buf)

                self.sleep(3600)
            else:
                self.sleep(3600)
