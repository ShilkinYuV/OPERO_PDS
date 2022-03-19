from datetime import datetime
import os
import re
from time import sleep, time
from tokenize import group
from xml.dom import minidom
from PyQt5.QtCore import QThread
from PyQt5 import QtCore, QtWidgets, QtGui
import socket
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

    def __init__(self, form, settings_path, handle_check=False):
        QThread.__init__(self)
        self.form = form
        self.settings_path = settings_path
        self.fe = FileExplorer()
        self.handle_check = handle_check

    def run(self):
        """Проверка доступности хоста"""
        work = True
        while work:
            regular = re.compile(r"http:\/\/(?P<ip>.*)\:(?P<port>.*)\/get")
            self.fe.check_dir(self.settings_path)
            if os.path.exists(self.settings_path + 'arm.cfg') == False:
                self.log_str.emit("Не могу найти arm.cfg для теста VPN", LogType.ERROR)
            if os.path.isfile(self.settings_path + 'arm.cfg'):
                mydoc = minidom.parse(self.settings_path + 'arm.cfg')
                items = mydoc.getElementsByTagName("svk-httpServerFrom")
                for elem in items:
                    elementXML = str(elem.firstChild.data)
                    groups = regular.match(elementXML).groups('ip')
                    print(groups)
                    if self.CheckHost((str(groups[0]),int(groups[1]))) == False:
                        self.log_str.emit("", LogType.SPACE)
                        self.log_str.emit("Vpn соединение недоступно", LogType.ERROR)
                    else: 
                        self.log_str.emit("", LogType.SPACE)
                        self.log_str.emit("Vpn соединение доступно", LogType.INFO)
                        
            if self.handle_check == True:
                work = False
                self.form.ui.pbutton_check_vpn.setDisabled(False)
            else:
                sleep(4200)

    def ping(self, host):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        try:
            s.connect(host)
            s.shutdown(socket.SHUT_RDWR)
            return True
        except:
            return False
        finally:
            s.close()

        response = os.system("ping -n 3 -w 3000 {}".format(host))
        if response == 0:
            return True
        else:
            return False

    def CheckHost(self, host):
        ipup = False
        for i in range(5):
            if self.ping(host):
                ipup = True
                break
            else:
                sleep(5)
        
        return ipup