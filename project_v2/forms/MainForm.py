from xml.dom import minidom
from PyQt5 import QtWidgets, QtCore, QtGui
from libs.EpdNight import NightCicle
from ui_forms.MainWindow import Ui_MainWindow
from forms.AboutForm import AboutForm
import os

from datetime import datetime
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
from contants.doc_types import doc_types
from libs.FileExplorer import FileExplorer
from libs.Logger import Logger, CheckConnection


class MainForm(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super(MainForm, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.textEdit.setReadOnly(True)
        self.ui.day.clicked.connect(self.epd_day_start)
        self.ui.chekDocuments.clicked.connect(self.check_dirs)
        self.ui.night.clicked.connect(self.epd_night)

        self.ui.OTVSEND.clicked.connect(lambda: self.send_docs(doc_types["OTVSEND"]))
        self.ui.OTZVSEND.clicked.connect(lambda: self.send_docs(doc_types["OTZVSEND"]))
        self.ui.PESSEND.clicked.connect(lambda: self.send_docs(doc_types["PESSEND"]))
        self.ui.RNPSEND.clicked.connect(lambda: self.send_docs(doc_types["RNPSEND"]))
        self.ui.ZINFSEND.clicked.connect(lambda: self.send_docs(doc_types["ZINFSEND"]))
        self.ui.ZONDSEND.clicked.connect(lambda: self.send_docs(doc_types["ZONDSEND"]))
        self.ui.ZVPSEND.clicked.connect(lambda: self.send_docs(doc_types["ZVPSEND"]))

        self.about_form = None
        self.ui.pushButton_2.clicked.connect(self.open_about_form)
        self.press_button = False

        self.logger = Logger(file_log_path=dir_log, form_log_path=self.ui.textEdit)

        self.night_thread = None

        self.check_connection()

    def check_connection(self):
        """Проверка соединения"""
        self.check_conn = CheckConnection(dir_log, _logger=self.logger)
        self.check_conn.setDaemon(True)
        # self.check_conn.log_str.connect(self.logger.log)
        self.check_conn.start()

    def open_about_form(self):
        self.about_form = AboutForm()
        self.about_form.show()

    def epd_day_start(self):

        file_explorer = FileExplorer(_logger=self.logger)
        file_explorer.log_str.connect(self.log)
        file_explorer.check_dir(dir_log)
        file_explorer.check_dir(dir_armkbr + "\\exg\\rcv")

        current_date = datetime.now().strftime("%d.%m.%Y")

        if file_explorer.count_files_in_folder(dir_armkbr + "\\exg\\rcv") == 0:
            self.logger.log("Нет файлов к отправке!")

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
            file_explorer.copy_files(arm_buf, trans_disk_path, r".*ed211.*\.ed\.xml")

            file_explorer.copy_files(arm_buf, puds_disk + "input", r".*\.ed")
            file_explorer.copy_files(arm_buf, puds_disk + "input", r".*ed211.*\.eds")

            file_explorer.delete_files(arm_buf, r".*\.xml")

            file_explorer.copy_files(arm_buf, dir_armkbr + "\\exg\\rcv\\1")

            file_explorer.delete_files(arm_buf)

    def send_docs(self, rnp):
        """Отправка определенных документов выбираемых на RNP"""
        file_explorer = FileExplorer(_logger=self.logger)
        file_explorer.log_str.connect(self.log)

        current_date = datetime.now().strftime("%d%m%Y")

        vchera = trans_disk + "\\OUT_OEBS\\4800\\044525000\\" + current_date

        file_explorer.check_dir(vchera)

        vcheran = trans_disk + "\\OUT_OEBS\\4800\\004525987\\" + current_date

        file_explorer.check_dir(vcheran)

        count = 0

        count += file_explorer.check_dir_for_docs(
            rnp=rnp, path_from=vchera, path_to=CLI
        )
        count += file_explorer.check_dir_for_docs(
            rnp=rnp, path_from=vcheran, path_to=CLI
        )

        if count == 0:
            sender = self.sender()
            self.logger.log("Не найдено ни одного документа {}".format(sender.text()))

    def check_dirs(self):
        """Проверка директорий на наличие файлов"""
        file_explorer = FileExplorer(_logger=self.logger)
        file_explorer.log_str.connect(self.log)
        
        current_date = datetime.now().strftime("%d%m%Y")

        vchera = trans_disk + "\\OUT_OEBS\\4800\\044525000\\" + current_date
        vcheran = trans_disk + "\\OUT_OEBS\\4800\\004525987\\" + current_date

        file_explorer.check_dirs_for_send_docs(
            rnp_folders=[vchera, vcheran],
            rnp_doc_types=doc_types,
            dir_armkbrn=(dir_armkbr + "\\exg\\rcv"),
        )

    def epd_day2_start(self):

        fe = FileExplorer(_logger=self.logger)

        count_ed201 = fe.count_files_in_folder(dir_armkbr + "\\exg\\rcv", filter=r'.*ed201.*')

        if count_ed201 != 0:
            pass
            
        else:
            rcv = dir_armkbr + "\\Exg\\rcv"
            bvp = rcv + "\\211"

            dd = datetime.now().day

            fe.move_files(rcv,bvp,filter=r".*4525000987000000000000ED2114"+str(dd)+r"01.*\.ed")
            fe.move_files(rcv,bvp,filter=r".*4525000987000000000000ED2114"+str(dd)+r"02.*\.ed")
            fe.move_files(rcv,bvp,filter=r".*4525000987000000000000ED2114"+str(dd)+r"03.*\.ed")
            fe.move_files(rcv,bvp,filter=r".*4525000987000000000000ED2114"+str(dd)+r"04.*\.ed")

            fe.check_dir(dir_log)
            fe.check_dir(dir_armkbr + "\\exg\\rcv")

            if fe.count_files_in_folder(dir_armkbr + "\\exg\\rcv") == 0:
                self.logger.log("Нет файлов к отправке!")

            else:

                current_date = datetime.now().strftime("%d.%m.%Y")

                fe.check_dir(dir_archive)
                fe.check_dir(arm_buf)

                fe.move_files(dir_armkbr + "\\exg\\rcv", arm_buf)

                fe.decode_files(unb64_rabis, arm_buf, dir_log)

                arc_dir = dir_archive + "\\" + current_date + "\\uarm3\\inc\\ed"

                fe.check_dir(arc_dir)

                fe.copy_files(arm_buf, arc_dir, r".*\.ed\.xml")
                fe.copy_files(arm_buf, arc_dir, r".*ed211.*\.ed\.xml")

                trans_disk_path = trans_disk + "IN_OEBS_BIK\\044525000"

                rash = "D:\\rash\\ED808"

                fe.check_dir(rash)

                fe.copy_files(arm_buf, trans_disk_path, r".*\.ed\.xml")
                fe.copy_files(arm_buf, trans_disk_path, r".*ed211.*\.ed\.xml")
                fe.copy_files(arm_buf, rash, r".*ed808.*\.eds\.xml")

                fe.copy_files(arm_buf, puds_disk + "input", r".*\.ed")
                fe.copy_files(arm_buf, puds_disk + "input", r".*ed211.*\.eds")

                fe.delete_files(arm_buf, r".*\.xml")

                fe.copy_files(arm_buf, dir_armkbr + "\\exg\\rcv\\1")

                fe.delete_files(arm_buf)
                

            pass
        
    def epd_night(self):
        print("epd night")
        if self.press_button == False:
            self.ui.night.setStyleSheet('QPushButton {background-color: #8AB6D1;} QPushButton:hover {background-color: #607E91;}')

            self.night_thread = NightCicle(self.logger)
            self.night_thread.log_str.connect(self.log)
            self.night_thread.start()

            self.press_button = True
        else:
            self.press_button = False
            self.night_thread.work = False
            self.night_thread.quit()
            self.ui.night.setStyleSheet('QPushButton {background-color: #607E91;} QPushButton:hover {background-color: #8AB6D1;}')

    @QtCore.pyqtSlot(str, bool, bool)
    def log(self, message,isError, onlyInFile):
        self.logger.log(message,isError,onlyInFile)