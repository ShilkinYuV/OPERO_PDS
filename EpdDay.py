import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt6.QtGui import QIcon
import os
import shutil
import datetime
import logging


class EpdDay:

    def __init__(self, my_window):
        self.my_window = my_window
        self.my_window.ui.day.clicked.connect(self.go_epd_day)
        self.isBANK = 'D:\\OEV\\Exg\\rcv'
        self.inASFK = 'D:\\inASFK'
        self.inPUDS = 'D:\\inPUDS'

    def go_epd_day(self):
        print('день')
        try:
           os.system('D:\\OEV\\Exg\\rcv\\unb64_rabis.exe *.* D:\\OEV\\Exg\\rcv >> D:\\OEV\\Exg\\rcv\\logs\\decod.log')
        except Exception:
            print('Ошибка ебучая')