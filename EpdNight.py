import sys
from threading import Thread
from time import sleep

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
        self.current_time = datetime.datetime.now()
        self.today = datetime.datetime.now()
        self.tomorrow = self.today + datetime.timedelta(days=1)
        self.tomorow_morning = self.tomorrow.replace(hour=9, minute=0, second=0, microsecond=0)
        self.evening = datetime.datetime.now().replace(hour=18, minute=0, second=0, microsecond=0)

    def go_epd_night(self):
        nigthCicle = NigthCicle(nigth=self)
        nigthCicle.start()


class NigthCicle(Thread):
    def __init__(self, nigth):
        Thread.__init__(self)
        self.nigth = nigth

    def run(self):
        while self.nigth.current_time > self.nigth.evening and self.nigth.current_time < self.nigth.tomorow_morning:
            # тут вся движуха будет
            sleep(1800)

