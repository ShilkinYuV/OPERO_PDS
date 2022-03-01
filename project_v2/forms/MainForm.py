from xml.dom import minidom
from PyQt5 import QtWidgets, QtCore, QtGui
from libs.EpdNight import NightCicle
from libs.EpdDay import EpdDay
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
        self.ui.day.clicked.connect(self.epd_day2_start)
        self.ui.chekDocuments.clicked.connect(self.check_dirs)
        self.ui.night.clicked.connect(self.epd_night)
        self.ui.clearWindow.clicked.connect(self.ui.textEdit.clear)

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
        self.read_local_log()

    def read_local_log(self):
        """Чтение лога, при наличии и вывод в визуальную форму"""
        path = (
            dir_log + "\\1\\" + datetime.now().strftime("%Y%m%d") + "\\" + "sample.log"
        )
        if os.path.isfile(path):
            log = open(path, "r")
            num_lines = sum(1 for line in open(path))
            if num_lines == 0:
                self.ui.textEdit.append('По пути "{}" пустой лог '.format(path))
            else:
                print("start loop")
                for line in log:
                    # Делим строчку лога на тип, дату и сообщение
                    splitted = line.split("|")
                    type = splitted[0]
                    date_time = splitted[1].replace(splitted[1][19:26], "")
                    message = splitted[2]

                    if type.__contains__("ERROR") and not message.__contains__(
                        "CheckConnection"
                    ):
                        self.ui.textEdit.append(
                            "<font color='red'>{date} {message}</font>".format(
                                date=date_time, message=message
                            )
                        )

                    elif type.__contains__("INFO") and not message.__contains__(
                        "CheckConnection"
                    ):
                        self.ui.textEdit.append(
                            "<font color='white'>{date} {message}</font>".format(
                                date=date_time, message=message
                            )
                        )

        else:
            self.ui.textEdit.append('По пути "{}" отсутствует лог '.format(path))

    def check_connection(self):
        """Проверка соединения"""
        self.check_conn = CheckConnection(dir_log, _logger=self.logger)
        self.check_conn.setDaemon(True)
        # self.check_conn.log_str.connect(self.logger.log)
        self.check_conn.start()

    def open_about_form(self):
        self.about_form = AboutForm()
        self.about_form.show()

    def send_docs(self, rnp):
        """Отправка определенных документов выбираемых на RNP"""
        file_explorer = FileExplorer()
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
        file_explorer = FileExplorer()
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
        self.day_thread = EpdDay(form=self)
        self.day_thread.log_str.connect(self.log)
        self.day_thread.start()
        self.ui.day.setDisabled(True)

    def epd_night(self):
        print("epd night")
        if self.press_button == False:
            self.ui.night.setStyleSheet(
                "QPushButton {background-color: #8AB6D1;} QPushButton:hover {background-color: #607E91;}"
            )

            self.night_thread = NightCicle()
            self.night_thread.log_str.connect(self.log)
            self.night_thread.start()

            self.press_button = True
        else:
            self.press_button = False
            self.night_thread.work = False
            self.night_thread.quit()
            self.ui.night.setStyleSheet(
                "QPushButton {background-color: #607E91;} QPushButton:hover {background-color: #8AB6D1;}"
            )

    @QtCore.pyqtSlot(str, bool, bool)
    def log(self, message, isError, onlyInFile):
        self.logger.log(message, isError, onlyInFile)
