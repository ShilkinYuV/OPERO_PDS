import sys
from threading import Thread
from time import sleep
from turtle import update

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt6.QtGui import QIcon
import os
import shutil
import datetime
import logging

from path_constants import fromBANK, toPUDS, toASFK, decoderPath, decoderLogs


class EpdNight:

    def __init__(self, my_window):
        self.my_window = my_window
        self.my_window.ui.night.clicked.connect(self.go_epd_night)
        self.isBANK = fromBANK
        self.inASFK = toASFK
        self.inPUDS = toPUDS
        self.current_time = datetime.datetime.now()
        self.today = datetime.datetime.now()
        self.tomorrow = self.today + datetime.timedelta(days=1)
        self.tomorow_morning = self.tomorrow.replace(hour=9, minute=0, second=0, microsecond=0)
        self.evening = datetime.datetime.now().replace(hour=18, minute=0, second=0, microsecond=0)

    # метод запускает выполнение потока из класса NightCicle
    def go_epd_night(self):
        self.current_time = datetime.datetime.now()
        self.UpdateDate()
        nightCicle = NightCicle(night=self)
        nightCicle.start()

    # обновление переменных времени
    def UpdateDate(self):
        self.today = datetime.datetime.now()
        self.tomorrow = self.today + datetime.timedelta(days=1)
        self.tomorow_morning = self.tomorrow.replace(hour=9, minute=0, second=0, microsecond=0)
        self.evening = datetime.datetime.now().replace(hour=18, minute=0, second=0, microsecond=0)


# Класс поток для расшифровки документов от банка ночью вызывается в NightCicle
class NightCicle(Thread):
    def __init__(self, night):
        Thread.__init__(self)
        self.night = night

    def run(self):
        while True:
            self.current_time = datetime.datetime.now()
            if self.night.current_time > self.night.evening and self.night.current_time < self.night.tomorow_morning:

                files = os.listdir(self.night.isBANK)
                count_files_before = len(files)
                print(count_files_before)

                try:
                    os.system('{decoderPath} *.* {fromBank} >> {decoderLogs}'.format(fromBANK=fromBANK,
                                                                                     decoderPath=decoderPath,
                                                                                     decoderLogs=decoderLogs))
                except Exception:
                    print('Ошибка ебучая')

                files = os.listdir(self.night.isBANK)
                count_files_after = len(files)
                print(count_files_after)

                if count_files_before == 0:
                    self.night.my_window.ui.textEdit.append(
                        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Отсутсвуют файлы для расшифровки')
                    logging.info(
                        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Отсутсвуют файлы для расшифровки')

                elif count_files_after - count_files_before == count_files_before:
                    self.night.my_window.ui.textEdit.append(
                        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Расшифровка файлов успешно завершена')
                    logging.info(
                        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Расшифровка файлов успешно завершена')
                else:
                    self.night.my_window.ui.textEdit.append(datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S") + ' Не удалось расшифровать все файлы, из ' + str(
                        count_files_after) + " " + "Расшифровано " + str(count_files_after - count_files_before))
                    logging.error(datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S") + ' Не удалось расшифровать все файлы, из ' + str(
                        count_files_after) + " " + "Расшифровано " + str(count_files_after - count_files_before))

                sleep(1800)
            else:
                self.night.UpdateDate()
                sleep(1800)
