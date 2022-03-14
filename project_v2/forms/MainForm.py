from re import S
from xml.dom import minidom
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QSettings
import os

from libs.EpdNight import NightCicle
from libs.EpdDay import EpdDay
from libs.SendDocs import SendDocs
from libs.CheckDirs import CheckDirs
from libs.Logger import Logger, CheckConnection
from libs.LogType import LogType
from libs.CheckVPN import CheckVPN
from libs.PasswordNotify import PasswordNotify
from libs.DiskSpaceChecker import DiskSpaceChecker

from ui_forms.MainWindow import Ui_MainWindow
from forms.AboutForm import AboutForm

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
    vpn_settgins_folder
)
from contants.doc_types import doc_types
from contants.app_constants import app_name, app_version


class MainForm(QtWidgets.QMainWindow):

    def __init__(self) -> None:
        super(MainForm, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.settings = QSettings('OIS', app_name, self)

        self.ui.textEdit.setReadOnly(True)
        self.ui.day.clicked.connect(self.epd_day2_start)
        self.ui.chekDocuments.clicked.connect(self.check_dirs)
        self.ui.night.clicked.connect(self.epd_night)
        self.ui.clearWindow.clicked.connect(self.ui.textEdit.clear)
        self.ui.lbl_password_days.clicked.connect(self.reset_password_days)
        self.ui.pbutton_check_vpn.clicked.connect(self.hanlde_check_vpn)
        self.ui.OTVSEND.clicked.connect(
            lambda: self.send_docs(doc_types["OTVSEND"], False))
        self.ui.RNPSEND.clicked.connect(
            lambda: self.send_docs(doc_types["RNPSEND"], False))
        self.ui.OTZVSEND.clicked.connect(
            lambda: self.send_docs(doc_types["OTZVSEND"], False))
        self.ui.PESSEND.clicked.connect(
            lambda: self.send_docs(doc_types["PESSEND"], False))
        self.ui.ZINFSEND.clicked.connect(
            lambda: self.send_docs(doc_types["ZINFSEND"], False))
        self.ui.ZONDSEND.clicked.connect(
            lambda: self.send_docs(doc_types["ZONDSEND"], False))
        self.ui.ZVPSEND.clicked.connect(
            lambda: self.send_docs(doc_types["ZVPSEND"], False))

        self.ui.OTVSEND_PUDS.clicked.connect(
            lambda: self.send_docs(doc_types["OTVSEND_PUDS"], True))
        self.ui.RNPSEND_PUDS.clicked.connect(
            lambda: self.send_docs(doc_types["RNPSEND_PUDS"], True))
        self.ui.OTZVSEND_PUDS.clicked.connect(
            lambda: self.send_docs(doc_types["OTZVSEND"], True))
        self.ui.PESSEND_PUDS.clicked.connect(
            lambda: self.send_docs(doc_types["PESSEND"], True))
        self.ui.ZINFSEND_PUDS.clicked.connect(
            lambda: self.send_docs(doc_types["ZINFSEND"], True))
        self.ui.ZONDSEND_PUDS.clicked.connect(
            lambda: self.send_docs(doc_types["ZONDSEND"], True))
        self.ui.ZVPSEND_PUDS.clicked.connect(
            lambda: self.send_docs(doc_types["ZVPSEND"], True))

        self.ui.pbutton_load_log.clicked.connect(self.read_local_log)
        self.setWindowTitle("{} - v{}".format(app_name, app_version))
        self.day_thread = None

        self.about_form = None
        self.ui.pbutton_show_about.clicked.connect(self.open_about_form)
        self.press_button = False

        self.logger = Logger(file_log_path=dir_log,
                             form_log_path=self.ui.textEdit)

        self.night_thread = None
        self.check_vpn = None
        
        self.check_connection()
        self.read_local_log()
        self.epd_night()
        self.start_check_vpn()

        self.load_settings()
        

        self.password_notify_start()
        self.disk_space_checker_start()

    def load_settings(self):
        if self.settings.value('count_output') is not None:
            self.count_output = int(self.settings.value('count_output'))
        else:
            self.count_output = 0

        if self.settings.value('count_input') is not None:
            self.count_input = int(self.settings.value('count_input'))
        else:
            self.count_input = 0

        if self.settings.value('last_count_day') is not None:
            self.last_count_day = int(self.settings.value('last_count_day'))
            if self.last_count_day != datetime.now().day:
                self.last_count_day = datetime.now().day
                self.settings.setValue('last_count_day', self.last_count_day)
                self.settings.setValue('count_output', 0)
                self.settings.setValue('count_input', 0)
                self.count_input = 0
                self.count_output = 0
        else:
            self.last_count_day = datetime.now().day
            self.settings.setValue('last_count_day', self.last_count_day)


        if self.settings.value('last_date_password') is not None:
            self.last_date_password = self.settings.value('last_date_password')
            self.password_days_count = 45 - \
                (datetime.now() - self.last_date_password).days
        else:
            self.last_date_password = datetime.now()
            self.settings.setValue('last_date_password', self.last_date_password)
            self.password_days_count = 45

        self.ui.lbl_output_count.setText(
            'Отправлено: {}'.format(self.count_output))
        self.ui.lbl_inptut_count.setText(
            'Загружено: {}'.format(self.count_input))
        self.ui.lbl_password_days.setText(
            'Дней до смены пароля:  {}'.format(self.password_days_count))

    def hanlde_check_vpn(self):
        self.ui.pbutton_check_vpn.setDisabled(True)
        self.handle_check_vpn = CheckVPN(self, settings_path=vpn_settgins_folder, handle_check=True)
        self.handle_check_vpn.log_str.connect(self.log)
        self.handle_check_vpn.start()

    def reset_password_days(self):
        """Сброс счетчика дней до смены пароля"""
        reply = QMessageBox.question(self, "Сброс счетчика", "Сбросить счетчик дней до смены пароля?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.password_days_count = 45 - \
                (datetime.now() - datetime.now()).days
            self.settings.setValue('last_date_password', datetime.now())
            self.ui.lbl_password_days.setText(
                'Дней до смены пароля:  {}'.format(self.password_days_count))

    @QtCore.pyqtSlot()
    def update_password_days(self):
        """Слот для обновления счетчика дней смены пароля"""
        self.password_days_count = 45 - \
            (datetime.now() - self.last_date_password).days
        self.ui.lbl_password_days.setText(
            'Дней до смены пароля:  {}'.format(self.password_days_count))
        if self.password_days_count <= 3 and datetime.now().hour == 9:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Information)
            if self.password_days_count == 1:
                days = "день"
            elif self.password_days_count >= 2 and self.password_days_count <= 4:
                days = "дня"
            else:
                days = "дней"
            msg.setText("Пароль истекает через {} {}".format(
                self.password_days_count, days))
            msg.setWindowTitle("Требуется смена пароля!")

            msg.show()

    def password_notify_start(self):
        """Запуск потока проверки дней до смены пароля"""
        self.password_notify = PasswordNotify()
        self.password_notify.pswrd_days_count.connect(
            self.update_password_days)
        self.password_notify.start()

    def disk_space_checker_start(self):
        """Запуск потока проверки дней до смены пароля"""
        self.disk_space_checker = DiskSpaceChecker()
        self.disk_space_checker.msg_signal.connect(
            self.free_space_msg)
        self.disk_space_checker.start()

    def read_local_log(self):
        """Чтение лога, при наличии и вывод в визуальную форму"""
        self.ui.textEdit.clear()
        path = (
            dir_log + "\\1\\" + datetime.now().strftime("%Y%m%d") + "\\" + "visual.log"
        )
        if os.path.isfile(path):
            log = open(path, "r")
            num_lines = sum(1 for line in open(path))
            first = True
            if num_lines == 0:
                self.ui.textEdit.append(
                    'По пути "{}" пустой лог '.format(path))
            else:
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

                    elif type.__contains__("WARNING") and not message.__contains__(
                        "CheckConnection"
                    ):
                        self.ui.textEdit.append(
                            "<font color='orange'>{date} {message}</font>".format(
                                date=date_time, message=message
                            )
                        )
                    elif type.__contains__("FILES") and not message.__contains__(
                        "CheckConnection"
                    ):
                        self.ui.textEdit.append(
                            "<font color='lightgreen'>{message}</font>".format(
                                date=date_time, message=message
                            )
                        )
                    elif type.__contains__("SPACE") and not message.__contains__(
                        "CheckConnection"
                    ):
                        self.ui.textEdit.append(" ")

        else:
            self.ui.textEdit.append(
                'По пути "{}" отсутствует лог '.format(path))

    def check_connection(self):
        """Проверка соединения"""
        self.check_conn = CheckConnection(dir_log, _logger=self.logger)
        self.check_conn.setDaemon(True)
        self.check_conn.start()

    def open_about_form(self):
        self.about_form = AboutForm()
        self.about_form.show()

    def send_docs(self, rnp, isFromPuds):
        """Отправка доков по определенным РНП"""
        self.log('', LogType.SPACE)
        sender = self.sender()
        self.sendDocs = SendDocs(form=self, button=self.sender(
        ), rnp=rnp, doc_type=sender.text(), isFromPuds=isFromPuds)
        self.sendDocs.log_str.connect(self.log)
        self.sendDocs.update_counts.connect(self.update_counts)
        self.sendDocs.start()

    def check_dirs(self):
        """Проверка директорий на наличие файлов"""
        self.log('', LogType.SPACE)
        self.check_dirs = CheckDirs(form=self, doc_types=doc_types)
        self.check_dirs.log_str.connect(self.log)
        self.check_dirs.start()

    def epd_day2_start(self):
        """ЭПД дневное"""
        self.log('', LogType.SPACE)
        self.day_thread = EpdDay(form=self)
        self.day_thread.log_str.connect(self.log)
        self.day_thread.confir_message.connect(self.accept_form)
        self.day_thread.update_counts.connect(self.update_counts)
        self.day_thread.start()
        self.ui.day.setDisabled(True)

    def epd_night(self):
        if self.press_button == False:
            self.ui.night.setStyleSheet(
                "QPushButton {background-color: #8AB6D1;} QPushButton:hover {background-color: #607E91;}"
            )

            self.night_thread = NightCicle(form=self)
            self.night_thread.log_str.connect(self.log)
            self.night_thread.update_counts.connect(self.update_counts)
            self.night_thread.start()

            self.press_button = True
        else:
            reply = QMessageBox.question(self, "Отключить ЭПД ночной?", "Вы уверены, что хотите отключить ночной ЭПД?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.press_button = False
                self.night_thread.work = False
                self.night_thread.quit()
                self.ui.night.setStyleSheet(
                    "QPushButton {background-color: #607E91;} QPushButton:hover {background-color: #8AB6D1;}"
                )
            else:
                pass

    @QtCore.pyqtSlot(str, LogType)
    def log(self, message, log_type):
        self.logger.log(message, log_type=log_type)

    @QtCore.pyqtSlot(str)
    def free_space_msg(self, message):
        """Сообщение о свободном пространстве на диске"""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText(message)
        msg.setWindowTitle("Заканчивается свободное место на диске!")

        msg.show()

    @QtCore.pyqtSlot(int, int)
    def update_counts(self, output, input):
        if self.last_count_day != datetime.now().day:
            self.count_output = 0
            self.count_input = 0
            self.last_count_day = datetime.now().day

            self.count_output += output
            self.count_input += input
        else:
            self.count_output += output
            self.count_input += input

        self.settings.setValue('count_output', int(self.count_output))
        self.settings.setValue('count_input', int(self.count_input))
        self.settings.setValue('last_count_day', int(self.last_count_day))

        self.ui.lbl_output_count.setText(
            'Отправлено: {}'.format(self.count_output))
        self.ui.lbl_inptut_count.setText(
            'Загружено: {}'.format(self.count_input))

    @QtCore.pyqtSlot(str, str)
    def accept_form(self, title, message):
        reply = QMessageBox.question(self, title, message,
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.day_thread.confirm = True

        else:
            self.day_thread.confirm = False

    def start_check_vpn(self):
        self.check_vpn = CheckVPN(self, settings_path=vpn_settgins_folder)
        self.check_vpn.log_str.connect(self.log)
        self.check_vpn.start()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if self.night_thread is not None:
            self.night_thread.quit()
        if self.check_vpn is not None:
            self.check_vpn.quit()
