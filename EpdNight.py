import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt6.QtGui import QIcon
import os
import shutil
import datetime
import logging


class EpdNight:

    def __init__(self, my_window):
        self.my_window = my_window
        self.my_window.ui.night.clicked.connect(self.go_epd_night)
        self.isBANK = 'D:\\OEV\\Exg\\rcv'
        self.inASFK = 'D:\\inASFK'
        self.inPUDS = 'D:\\inPUDS'

    def go_epd_night(self):
        print('ночь')
