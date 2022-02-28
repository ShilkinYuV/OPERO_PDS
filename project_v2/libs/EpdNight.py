from datetime import datetime
from PyQt5.QtCore import QThread
from PyQt5 import QtCore

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

    def __init__(self, logger):
        QThread.__init__(self)
        self.work = True
        self.logger = logger

    def run(self):
        while self.work:
            current_hour = datetime.now().hour
            if current_hour < 9 and current_hour > 21:
                file_explorer = FileExplorer(_logger=self.logger)
                file_explorer.check_dir(dir_log)
                file_explorer.check_dir(dir_armkbr + "\\exg\\rcv")

                current_date = datetime.now().strftime("%d.%m.%Y")

                if file_explorer.count_files_in_folder(dir_armkbr + "\\exg\\rcv") == 0:
                    self.log_str.emit("Нет файлов к отправке!", False, False)

                else:
                    file_explorer.check_dir(dir_archive)
                    file_explorer.check_dir(arm_buf)

                    file_explorer.move_files(dir_armkbr + "\\exg\\rcv", arm_buf)

                    file_explorer.decode_files(unb64_rabis, arm_buf, dir_log)

                    arc_dir = dir_archive + "\\" + current_date + "\\uarm3\\inc\\ed"

                    file_explorer.check_dir(arc_dir)

                    file_explorer.copy_files(arm_buf, arc_dir, r".*\.ed\.xml")
                    file_explorer.copy_files(arm_buf, arc_dir, r".*ed211.*\.ed\.xml")

                    trans_disk_path = trans_disk + "IN_OEBS_BIK\\044525000"

                    file_explorer.copy_files(arm_buf, trans_disk_path, r".*\.ed\.xml")
                    file_explorer.copy_files(
                        arm_buf, trans_disk_path, r".*ed211.*\.ed\.xml"
                    )

                    file_explorer.copy_files(arm_buf, puds_disk + "input", r".*\.ed")
                    file_explorer.copy_files(
                        arm_buf, puds_disk + "input", r".*ed211.*\.eds"
                    )

                    file_explorer.delete_files(arm_buf, r".*\.xml")

                    file_explorer.copy_files(arm_buf, dir_armkbr + "\\exg\\rcv\\1")

                    file_explorer.delete_files(arm_buf)

                self.sleep(1800)
            else:
                self.sleep(1800)
