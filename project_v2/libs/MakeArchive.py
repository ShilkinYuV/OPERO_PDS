from datetime import datetime
from PyQt5.QtCore import QThread
from PyQt5 import QtCore


class MakeArchive(QThread):

    def __init__(self):
        QThread.__init__(self)

    def run(self):
        """Создание архива"""
        while True:

            pass