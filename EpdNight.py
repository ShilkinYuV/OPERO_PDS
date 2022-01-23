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
        # while True:
            files = os.listdir(self.nigth.isBANK)
            count_files_before = len(files)
            print(count_files_before)

            try:
                os.system('D:\\OEV\\Exg\\unb64_rabis.exe *.* D:\\OEV\\Exg\\rcv >> D:\\OEV\\Exg\\logs\\decod.log')
            except Exception:
                print('Ошибка ебучая')

            files = os.listdir(self.nigth.isBANK)
            count_files_after = len(files)
            print(count_files_after)

            if count_files_before == 0:
                self.nigth.my_window.ui.textEdit.append(
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Отсутсвуют файлы для расшифровки')
                logging.info(
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Отсутсвуют файлы для расшифровки')

            elif count_files_after - count_files_before == count_files_before:
                self.nigth.my_window.ui.textEdit.append(
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Расшифровка файлов успешно завершена')
                logging.info(
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Расшифровка файлов успешно завершена')
            else:
                self.nigth.my_window.ui.textEdit.append(datetime.datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S") + ' Не удалось расшифровать все файлы, из ' + str(
                    count_files_after) + " " + "Расшифровано " + str(count_files_after - count_files_before))
                logging.error(datetime.datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S") + ' Не удалось расшифровать все файлы, из ' + str(
                    count_files_after) + " " + "Расшифровано " + str(count_files_after - count_files_before))
            sleep(1800)
