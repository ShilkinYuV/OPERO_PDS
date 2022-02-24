from ast import Try
import sys
from threading import Thread
from time import sleep
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QObject
import os
import shutil
import datetime
import logging

from path_constants import fromBANK, toPUDS, toASFK, decoderPath, decoderLogs, fromBANKBuff, fromBankArhive


class EpdNight(QObject):
    log_str = QtCore.pyqtSignal(str, bool)

    def __init__(self, my_window):
        super(EpdNight, self).__init__()
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
        self.pressButton = False

    # метод запускает выполнение потока из класса NightCicle
    def go_epd_night(self):
        self.current_time = datetime.datetime.now()
        self.UpdateDate()
        nightCicle = NightCicle(night=self)
        nightCicle.setDaemon(True)
        nightCicle.start()

    # обновление переменных времени
    def UpdateDate(self):
        self.today = datetime.datetime.now()
        self.tomorrow = self.today + datetime.timedelta(days=1)
        self.tomorow_morning = self.tomorrow.replace(hour=9, minute=0, second=0, microsecond=0)
        self.evening = datetime.datetime.now().replace(hour=18, minute=0, second=0, microsecond=0)

    # Расшифровка файлов
    def decodeFiles(self):
        # Проверка количества документов в каталоге isBank до декодирования
        files = os.listdir(self.isBANK)
        count_files_before = len(files)
        print(count_files_before)
        for file in files:
            shutil.move(self.isBANK + '\\' + file, fromBANKBuff)
            # Декодирование
            command = '{decoderPath} *.* {fromBANKBuff} >> {decoderLogs}'.format(fromBANK=fromBANK,
                                                                                                decoderPath=decoderPath,
                                                                                                decoderLogs=decoderLogs,
                                                                                                fromBANKBuff=fromBANKBuff)
            try:
                os.system(command)
            except Exception:
                print('Ошибка ебучая')

            # Проверка количества документов в каталоге isBank после декодирования
            files = os.listdir(fromBANKBuff)
            count_files_after = len(files)
            print(count_files_after)
            # Сравнение количества документов до и после декодирования, логирование и вывод на экран
            if count_files_before == 0:
                self.log_str.emit('|'+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + '| Отсутсвуют файлы для расшифровки', True)
            elif count_files_after - 2 == count_files_before:
                self.log_str.emit('|'+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + '| Расшифровка файлов успешно завершена', True)
            else:
                self.log_str.emit('|'+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + '| Не удалось расшифровать все файлы, из ' + str(
                        count_files_after) + " " + "Расшифровано " + str((count_files_after - 2) - count_files_before), False)

    # Копирование в архивные папки
    def copyArhive(self):
        current_date_arhive_directory_ed = fromBankArhive + '\\' + datetime.datetime.now().strftime(
            "%Y%m%d") + '\\uarm3\\\inc\\ed'
        typefiles = os.listdir(fromBANKBuff)
        for file in typefiles:
            print(file)
            if file.__contains__('ED.xml') or (file.__contains__('ED211') and file.__contains__('EDS.xml')):
                if not os.path.exists(current_date_arhive_directory_ed):
                    os.makedirs(current_date_arhive_directory_ed)
                try:
                    shutil.copy2(fromBANKBuff + '\\' + file, current_date_arhive_directory_ed)
                    self.log_str.emit('|'+datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S.%f") + '| Копирование ' + file + ' из ' + fromBANKBuff + '\n' + ' в ' + (
                                                        fromBankArhive + '\\' + datetime.datetime.now().strftime(
                                                    "%Y%m%d")) + ' успешно завершено', True)
                except Exception:
                    self.log_str.emit('|'+datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S.%f") + '| Копирование ' + file + ' из ' + fromBANKBuff + '\n' + ' в ' + (
                                                    fromBankArhive + '\\' + datetime.datetime.now().strftime(
                                                "%Y%m%d")) + ' не удалось', False)

    # подключение сетевых дисков
    def mapping_network_drives(self):
        os.system('set trans_disk=x:')
        os.system('set puds_disk=w:')
        os.system('net use %trans_disk% /delete /y')
        os.system('net use %puds_disk% /delete /y')
        os.system('net use x: \\\\10.48.4.241\\transportbanks 1!QQww /USER:10.48.4.241\\svc95004800')
        os.system('net use w: \\\\10.48.4.241\\transport 1!QQww /USER:10.48.4.241\\svc95004800')

    # копирование в целевой каталог
    def copyInASFKAndPUDS(self):
        chekFileToASFK = False
        chekFileToPUDS = False
        files = os.listdir(fromBANKBuff)
        for file in files:
            myFile = fromBANKBuff + '\\' + file
            if file.__contains__('ED.xml') or (file.__contains__('ED211') and file.__contains__('EDS.xml')):
                try:
                    shutil.copy2(fromBANKBuff + '\\' + file, toASFK)
                except Exception:
                    self.log_str.emit('|'+datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S.%f") + '| Копирование ' + file + ' из ' + fromBANKBuff + '\n' + ' в ' + toASFK + ' не удалось', False)
                try:
                    shutil.copy2(fromBANKBuff + '\\' + file, toPUDS)
                except Exception:
                    self.log_str.emit('|'+datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S.%f") + '| Копирование ' + file + ' из ' + fromBANKBuff + '\n' + ' в ' + toPUDS + ' не удалось', False)

                filesToASFK = os.listdir(toASFK)
                for fileToASFK in filesToASFK:
                    if fileToASFK.__contains__(file):
                        self.log_str.emit('|'+datetime.datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S.%f") + '| Файл ' + file + ' присутствует в ' + toASFK, True)
                        chekFileToASFK = True

                filesToPUDS = os.listdir(toPUDS)
                for fileToPUDS in filesToPUDS:
                    if fileToASFK.__contains__(file):
                        self.log_str.emit('|'+datetime.datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S.%f") + '| Файл ' + file + ' присутствует в ' + toPUDS, True)
                        chekFileToPUDS = True

                if chekFileToASFK and chekFileToPUDS:
                    try:
                        os.remove(myFile)
                        self.log_str.emit('|'+datetime.datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S.%f") + '| Файл ' + file + ' удален из ' + fromBANKBuff, True)
                        chekArhive = False
                    except:
                        self.log_str.emit('|'+datetime.datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S.%f") + '| Не удалось удалить ' + file + ' из ' + fromBANKBuff, False)
                        chekArhive = False
            try:
                shutil.move(fromBANKBuff + '\\' + file, fromBANKBuff + '\\' + '1')
            except Exception:
                pass

# Класс поток для расшифровки документов от банка ночью вызывается в NightCicle
class NightCicle(Thread):
    log_str = QtCore.pyqtSignal(str)
    def __init__(self, night):
        Thread.__init__(self)
        self.night = night
        if self.night.pressButton:
            self.night.pressButton = False
            self.night.my_window.ui.night.setStyleSheet('QPushButton {background-color: #607E91;} QPushButton:hover {background-color: #8AB6D1;}')

        else:
            self.night.pressButton = True
            self.night.my_window.ui.night.setStyleSheet('QPushButton {background-color: #8AB6D1;} QPushButton:hover {background-color: #607E91;}')

    def run(self):
        while True:
            if not self.night.pressButton:
                break
            self.current_time = datetime.datetime.now()
            if self.night.current_time > self.night.evening and self.night.current_time < self.night.tomorow_morning:
            # if True:
                self.night.decodeFiles()
                self.night.copyArhive()
                self.night.mapping_network_drives()
                self.night.copyInASFKAndPUDS()
                sleep(1800)
            else:
                self.night.UpdateDate()
                sleep(1800)
