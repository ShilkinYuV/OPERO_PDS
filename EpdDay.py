import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt6.QtGui import QIcon
import os
import shutil
import datetime
import logging
from path_constants import fromBANK, toPUDS, toASFK, decoderPath, decoderLogs

class EpdDay:

    def __init__(self, my_window):
        self.my_window = my_window
        self.my_window.ui.day.clicked.connect(self.go_epd_day)
        self.isBANK = fromBANK
        self.inASFK = toASFK
        self.inPUDS = toPUDS

    def go_epd_day(self):
        print('день')
        files = os.listdir(self.isBANK)
        count_files_before = len(files)
        print(count_files_before)

        try:
           os.system('{decoderPath} *.* {fromBank} >> {decoderLogs}'.format(fromBANK=fromBANK,decoderPath=decoderPath,decoderLogs=decoderLogs))
        except Exception:
            print('Ошибка ебучая')

        files = os.listdir(self.isBANK)
        count_files_after = len(files)
        print(count_files_after)

        if count_files_before == 0:
            self.my_window.ui.textEdit.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Отсутсвуют файлы для расшифровки')
            logging.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Отсутсвуют файлы для расшифровки')

        elif count_files_after - count_files_before == count_files_before:
            self.my_window.ui.textEdit.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Расшифровка файлов успешно завершена')
            logging.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Расшифровка файлов успешно завершена')
        else:
            self.my_window.ui.textEdit.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Не удалось расшифровать все файлы, из ' + str(count_files_after) + " " + "Расшифровано " + str(count_files_after - count_files_before))
            logging.error(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Не удалось расшифровать все файлы, из ' + str(count_files_after) + " " + "Расшифровано " + str(count_files_after - count_files_before))