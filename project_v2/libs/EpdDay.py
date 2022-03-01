from datetime import datetime
from PyQt5.QtCore import QThread
from PyQt5 import QtCore, QtWidgets, QtGui

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


class EpdDay(QThread):

    log_str = QtCore.pyqtSignal(str, bool, bool)

    def __init__(self, form):
        QThread.__init__(self)
        self.form = form
        self.fe = FileExplorer()
        self.fe.log_str.connect(form.log)

    def run(self):

        now_hour = datetime.now().hour
        now_minutes = datetime.time(datetime.now()).__str__()

        if now_hour != 16:
            self.stage1()

        elif now_hour == 16:
            if now_minutes == 4 or now_minutes == 5:
                self.stage1()
            else:
                question = QtGui.QMessageBox.question(
                    self,
                    "",
                    'C 16:00 до 16:30 обычно происходит формирование "ППБ". Вы уверены что хотите продолжить загрузку?',
                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No 
                )

        self.form.ui.day.setDisabled(False)

    def stage1(self):
        count = self.fe.count_files_in_folder(
            dir_armkbr + "\\exg\\rcv", filter=r".*ed201.*"
        )
        if count != 0:
            self.stage3()
        else:
            self.stage2()

    def stage2(self):

        rcv = dir_armkbr + "\\Exg\\rcv"
        bvp = rcv + "\\211"

        dd = datetime.now().strftime('%d')

        print(dd)

        self.fe.move_files(
            rcv, bvp, filter=r".*4525000987000000000000ed2114" + str(dd) + r"01.*\.ed$"
        )
        self.fe.move_files(
            rcv, bvp, filter=r".*4525000987000000000000ed2114" + str(dd) + r"02.*\.ed$"
        )
        self.fe.move_files(
            rcv, bvp, filter=r".*4525000987000000000000ed2114" + str(dd) + r"03.*\.ed$"
        )
        self.fe.move_files(
            rcv, bvp, filter=r".*4525000987000000000000ed2114" + str(dd) + r"04.*\.ed$"
        )
        self.fe.move_files(rcv, bvp, filter=r".*ed211" + str(dd) + r".*\.eds$")

        self.fe.check_dir(dir_log)
        self.fe.check_dir(dir_armkbr + "\\exg\\rcv")

        if self.fe.count_files_in_folder(dir_armkbr + "\\exg\\rcv") == 0:
            self.log_str.emit("Нет файлов к отправке!", False, False)

        else:
            current_date = datetime.now().strftime("%d.%m.%Y")

            self.fe.check_dir(dir_archive)
            self.fe.check_dir(arm_buf)

            self.fe.move_files(dir_armkbr + "\\exg\\rcv", arm_buf)

            self.fe.decode_files(unb64_rabis, arm_buf, dir_log)

            arc_dir = dir_archive + "\\" + current_date + "\\uarm3\\inc\\ed"

            self.fe.check_dir(arc_dir)

            self.fe.copy_files(arm_buf, arc_dir, r".*\.ed\.xml$")
            self.fe.copy_files(arm_buf, arc_dir, r".*ed211.*\.ed\.xml$")

            trans_disk_path = trans_disk + "IN_OEBS_BIK\\044525000"

            rash = "D:\\rash\\ED808"

            self.fe.check_dir(rash)

            self.fe.copy_files(arm_buf, trans_disk_path, r".*\.ed\.xml$")
            self.fe.copy_files(arm_buf, trans_disk_path, r".*ed211.*\.ed\.xml$")
            self.fe.copy_files(arm_buf, rash, r".*ed808.*\.eds\.xml$")

            self.fe.copy_files(arm_buf, puds_disk + "input", r".*\.ed$")
            self.fe.copy_files(arm_buf, puds_disk + "input", r".*ed211.*\.eds$")

            self.fe.delete_files(arm_buf, r".*\.xml$")

            self.fe.copy_files(arm_buf, dir_armkbr + "\\exg\\rcv\\1")

            self.fe.delete_files(arm_buf)

    def stage3(self):
        pass
