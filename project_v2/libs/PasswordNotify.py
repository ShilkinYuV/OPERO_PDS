from datetime import datetime
from PyQt5.QtCore import QThread
from PyQt5 import QtCore


class PasswordNotify(QThread):

    pswrd_days_count = QtCore.pyqtSignal(int)

    def __init__(self):
        QThread.__init__(self)
        self.last_decreased_day = datetime.now().day

    def run(self):
        """Счетчик дней до смены пароля"""
        while True:
            if datetime.now().hour == 9 and self.last_decreased_daty != datetime.now().day:
                self.pswrd_days_count.emit(1)

            # elif self.last_decreased_daty != datetime.now().day:
            #     self.pswrd_days_count.emit(datetime.now().day - self.last_decreased_daty)

            self.sleep(1800)
       