from PyQt5 import QtWidgets, QtCore, QtGui
from ui_forms.MainWindow import Ui_MainWindow
import os

from datetime import datetime
from contants.path_constants import (
    dir_log,
    dir_armkbr,
    dir_archive,
    arm_buf,
    unb64_rabis,
    trans_disk,
    puds_disk
)
from libs.FileExplorer import FileExplorer
from libs.Logger import Logger


class MainForm(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super(MainForm, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.textEdit.setReadOnly(True)
        self.ui.day.clicked.connect(self.epd_day_start)
        


    def epd_day_start(self):

        logger = Logger(form_log_path=self.ui.textEdit)

        file_explorer = FileExplorer(_logger=logger)
        file_explorer.check_dir(dir_log)
        file_explorer.check_dir(dir_armkbr + "\\exg\\rcv")

        current_date = datetime.now().strftime("%d.%m.%Y")

        if file_explorer.count_files_in_folder(dir_armkbr + "\\exg\\rcv") == 0:
            print("Нет файлов по директории арм кбрн")

        else:
            file_explorer.check_dir(dir_archive)
            file_explorer.check_dir(arm_buf)

            file_explorer.move_files(dir_armkbr + "\\exg\\rcv", arm_buf)
            
            os.system(
                "{decoder} *.* {buffer}\ {buffer}\ >> {logs}\decod.log".format(
                    decoder=unb64_rabis, buffer=arm_buf, logs=dir_log
                )
            )

            arc_dir = dir_archive + "\\" + current_date + "\\uarm3\\inc\\ed"

            file_explorer.check_dir(arc_dir)

            file_explorer.copy_files(arm_buf, arc_dir, r".*\.ed\.xml")
            file_explorer.copy_files(arm_buf, arc_dir, r".*ed211.*\.ed\.xml")

            trans_disk_path = trans_disk + "IN_OEBS_BIK\\044525000"

            file_explorer.copy_files(arm_buf, trans_disk_path, r".*\.ed\.xml")
            file_explorer.copy_files(arm_buf, trans_disk_path, r".*ed211.*\.ed\.xml")

            file_explorer.copy_files(arm_buf, puds_disk + "input", r".*\.ed")
            file_explorer.copy_files(arm_buf, puds_disk + "input", r".*ed211.*\.eds")

            file_explorer.delete_files(arm_buf, r".*\.xml")

            file_explorer.copy_files(arm_buf, dir_armkbr + "\\exg\\rcv\\1")

            file_explorer.delete_files(arm_buf)


