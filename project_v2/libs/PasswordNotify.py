from datetime import datetime
from PyQt5.QtCore import QThread
from PyQt5 import QtCore


class PasswordNotify(QThread):

    pswrd_days_count = QtCore.pyqtSignal()

    def __init__(self):
        QThread.__init__(self)

    def run(self):
        """Счетчик дней до смены пароля"""
        while True:
            self.pswrd_days_count.emit()
                
            self.sleep(1800)
       