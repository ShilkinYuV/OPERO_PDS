from datetime import datetime
import os
import re
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
from libs.LogType import LogType


class CheckVPN(QThread):

    log_str = QtCore.pyqtSignal(str, LogType)

    def __init__(self, form, settings_path):
        QThread.__init__(self)
        self.form = form
        self.settings_path = settings_path
        self.fe = FileExplorer()

    def run(self):
        """Проверка доступности хоста"""
        while True:
            regular = re.compile(r"http:\/\/(?P<ip>.*)\:.*\/get")
            self.fe.check_dir(self.settings_path)
            if os.path.exists(self.settings_path + 'arm.cfg') == False:
                self.log_str.emit("Не могу найти arm.cfg для теста VPN", LogType.INFO)
            if os.path.isfile(self.settings_path + 'arm.cfg'):
                mydoc = minidom.parse(self.settings_path + 'arm.cfg')
                items = mydoc.getElementsByTagName("svk-httpServerFrom")
                for elem in items:
                    elementXML = str(elem.firstChild.data)
                    ip = regular.match(elementXML).groups('ip')
                    if self.ping(str(ip[0])) == False:
                        self.log_str.emit("", LogType.INFO)
                        self.log_str.emit("Vpn соединение недоступно", LogType.ERROR)
                        
            sleep(600)

    def ping(self, host):
        response = os.system("ping " + host)
        if response == 0:
            return True
        else:
            return False
