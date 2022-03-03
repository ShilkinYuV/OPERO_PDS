from datetime import datetime
import os
from time import sleep
from xml.dom import minidom
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


class CheckVPN(QThread):

    log_str = QtCore.pyqtSignal(str, bool, bool)

    def __init__(self, form, hosts, settings_path):
        QThread.__init__(self)
        self.form = form
        self.hosts = hosts
        self.settings_path = settings_path
        self.fe = FileExplorer()
        self.fe.log_str.connect(self.form.log)

    def run(self):
        """Проверка доступности хоста"""
        while True:
            self.fe.check_dir(self.settings_path)
            if os.path.exists(self.settings_path + 'preferences_global.xml') == False:
                self.log_str.emit("Не могу найти настройки", False, False)
            if os.path.isfile(self.settings_path + 'preferences_global.xml'):
                mydoc = minidom.parse(self.settings_path + 'preferences_global.xml')
                items = mydoc.getElementsByTagName("DefaultHostName")
                for elem in items:
                    elementXML = str(elem.firstChild.data)
                    if self.ping(elementXML) != 0:
                        self.log_str.emit("Vpn соединение недоступно", True, False)
                        
            sleep(600)

    def ping(self, host):
        response = os.system("ping " + host)
        if response == 0:
            return True
        else:
            return False
