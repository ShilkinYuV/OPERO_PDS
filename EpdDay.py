import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt6.QtGui import QIcon
import os
import shutil
import datetime
import logging
from path_constants import fromBANK, toPUDS, toASFK, decoderPath, decoderLogs, fromBANKBuff, fromBankArhive

class EpdDay:

    def __init__(self, my_window):
        self.my_window = my_window
        self.my_window.ui.day.clicked.connect(self.go_epd_day)
        self.isBANK = fromBANK
        self.inASFK = toASFK
        self.inPUDS = toPUDS

    # Расшифровка документов от банка днем
    def go_epd_day(self):
        print('день')
        # Проверка количества документов в каталоге isBank до декодирования
        files = os.listdir(self.isBANK)
        count_files_before = len(files)
        print(count_files_before)
        # Декодирование
        command = '{decoderPath} *.* {fromBANK} D:\\OEV\\Exg\\buff >> {decoderLogs}'.format(fromBANK=fromBANK,decoderPath=decoderPath,decoderLogs=decoderLogs, fromBANKBuff=fromBANKBuff)
        try:
           os.system(command)
        except Exception:
            print('Ошибка ебучая')
        # Проверка количества документов в каталоге isBank после декодирования
        files = os.listdir('D:\\OEV\\Exg\\buff')
        count_files_after = len(files)
        print(count_files_after)
        # Сравнение количества документов до и после декодирования, логирование и вывод на экран
        if count_files_before == 0:
            self.my_window.ui.textEdit.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Отсутсвуют файлы для расшифровки')
            logging.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Отсутсвуют файлы для расшифровки')

        elif count_files_after == count_files_before:
            self.my_window.ui.textEdit.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Расшифровка файлов успешно завершена')
            logging.info(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Расшифровка файлов успешно завершена')
        else:
            self.my_window.ui.textEdit.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Не удалось расшифровать все файлы, из ' + str(count_files_after) + " " + "Расшифровано " + str(count_files_after - count_files_before))
            logging.error(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Не удалось расшифровать все файлы, из ' + str(count_files_after) + " " + "Расшифровано " + str(count_files_after - count_files_before))

        current_date_arhive_directory_esid = fromBankArhive + '\\' + datetime.datetime.now().strftime("%Y%m%d") + '\\uarm3\\\inc\\esid'
        current_date_arhive_directory_epd = fromBankArhive + '\\' + datetime.datetime.now().strftime("%Y%m%d") + '\\uarm3\\\inc\\epd'
        current_date_arhive_directory_ed = fromBankArhive + '\\' + datetime.datetime.now().strftime("%Y%m%d") + '\\uarm3\\\inc\\ed'
        current_date_arhive_directory_vip = fromBankArhive + '\\' + datetime.datetime.now().strftime("%Y%m%d") + '\\uarm3\\\inc\\vip'
        current_date_arhive_directory_vip_itog = fromBankArhive + '\\itogday\\1\\VIPISKA'

        typefiles = os.listdir(fromBANKBuff)
        for file in typefiles:
            print(file)
            if file.__contains__('ESID.xml'):
                if not os.path.exists(current_date_arhive_directory_esid):
                    os.makedirs(current_date_arhive_directory_esid)
                shutil.copy2(fromBANKBuff + '\\' + file, current_date_arhive_directory_esid)
            elif file.__contains__('EPD.xml'):
                if not os.path.exists(current_date_arhive_directory_epd):
                    os.makedirs(current_date_arhive_directory_epd)
                shutil.copy2(fromBANKBuff + '\\' + file, current_date_arhive_directory_epd)
            elif file.__contains__('ED.xml') or file.__contains__('ED211') or file.__contains__('EDS.xml'):
                if not os.path.exists(current_date_arhive_directory_ed):
                    os.makedirs(current_date_arhive_directory_ed)
                shutil.copy2(fromBANKBuff + '\\' + file, current_date_arhive_directory_ed)
            elif file.__contains__('VIP.xml'):
                if not os.path.exists(current_date_arhive_directory_vip):
                    os.makedirs(current_date_arhive_directory_vip)
                if not os.path.exists(current_date_arhive_directory_vip_itog):
                    os.makedirs(current_date_arhive_directory_vip_itog)
                shutil.copy2(fromBANKBuff + '\\' + file, current_date_arhive_directory_vip)
                shutil.copy2(fromBANKBuff + '\\' + file, current_date_arhive_directory_vip_itog)