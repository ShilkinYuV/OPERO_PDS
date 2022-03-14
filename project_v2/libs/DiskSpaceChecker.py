from datetime import datetime
from PyQt5.QtCore import QThread
from PyQt5 import QtCore
import shutil

class DiskSpaceChecker(QThread):

    msg_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        QThread.__init__(self)

    def run(self):
        """Счетчик дней до смены пароля"""
        while True:
            total, used, free = shutil.disk_usage("D:\\")
            free = free//(2**30)
            if free < 15:
                self.msg_signal.emit("Свободное место на диске D = {} ГБ".format(free))
            self.sleep(1800)
       