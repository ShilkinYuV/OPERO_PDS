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

    def __init__(self, form, hosts):
        QThread.__init__(self)
        self.form = form
        self.hosts = hosts

    def run(self):
        """Проверка доступности хоста"""
        while True:
            isOneOfHostsPings = False
            for host in self.hosts:
                if self.ping(host):
                    isOneOfHostsPings = True
                else:
                    pass

            if isOneOfHostsPings == False:
                self.log_str.emit("Vpn соединение недоступно", True, False)

            sleep(600)

    def ping(self, host):
        response = os.system("ping " + host)
        if response == 0:
            return True
        else:
            return False
