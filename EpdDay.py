import sys
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt6.QtGui import QIcon
import os
import shutil
import datetime
import logging
from path_constants import fromBANK, toPUDS, toASFK, decoderPath, decoderLogs, fromBANKBuff, fromBankArhive


class EpdDay(QObject):
    log_str = QtCore.pyqtSignal(str)

    def __init__(self, my_window):
        super(EpdDay, self).__init__()
        self.my_window = my_window
        self.my_window.ui.day.clicked.connect(self.go_epd_day)
        self.isBANK = fromBANK
        self.inASFK = toASFK
        self.inPUDS = toPUDS

    # Расшифровка документов от банка днем
    def go_epd_day(self):
        print('день')
        self.decodeFiles()
        self.copyArhive()
        # self.mapping_network_drives()
        self.copyInASFKAndPUDS()

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
                self.log_str.emit(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Отсутсвуют файлы для расшифровки')
            elif count_files_after - 2 == count_files_before:
                self.log_str.emit(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Расшифровка файлов успешно завершена')
            else:
                self.log_str.emit(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Не удалось расшифровать все файлы, из ' + str(
                        count_files_after) + " " + "Расшифровано " + str((count_files_after - 2) - count_files_before))

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
                    self.my_window.ui.textEdit.append(datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S") + ' Копирование ' + file + ' из ' + fromBANKBuff + '\n' + ' в ' + (
                                                        fromBankArhive + '\\' + datetime.datetime.now().strftime(
                                                    "%Y%m%d")) + ' успешно завершено')
                    logging.info(datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S") + ' Копирование ' + file + ' из ' + fromBANKBuff + ' в ' + (
                                             fromBankArhive + '\\' + datetime.datetime.now().strftime(
                                         "%Y%m%d")) + ' успешно завершено')
                except Exception:
                    self.my_window.ui.textEdit.append(datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S") + ' Копирование ' + file + ' из ' + fromBANKBuff + '\n' + ' в ' + (
                                                    fromBankArhive + '\\' + datetime.datetime.now().strftime(
                                                "%Y%m%d")) + ' не удалось')
                    logging.error(datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S") + ' Копирование ' + file + ' из ' + fromBANKBuff + ' в ' + (
                                          fromBankArhive + '\\' + datetime.datetime.now().strftime(
                                      "%Y%m%d")) + ' не удалось')

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
                    self.log_str.emit(datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S") + ' Копирование ' + file + ' из ' + fromBANKBuff + '\n' + ' в ' + toASFK + ' не удалось')
                try:
                    shutil.copy2(fromBANKBuff + '\\' + file, toPUDS)
                except Exception:
                    self.log_str.emit(datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S") + ' Копирование ' + file + ' из ' + fromBANKBuff + '\n' + ' в ' + toPUDS + ' не удалось')

                filesToASFK = os.listdir(toASFK)
                for fileToASFK in filesToASFK:
                    if fileToASFK.__contains__(file):
                        self.log_str.emit(datetime.datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S") + ' Файл ' + file + ' присутствует в ' + toASFK)
                        chekFileToASFK = True

                filesToPUDS = os.listdir(toPUDS)
                for fileToPUDS in filesToPUDS:
                    if fileToASFK.__contains__(file):
                        self.log_str.emit(datetime.datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S") + ' Файл ' + file + ' присутствует в ' + toPUDS)
                        chekFileToPUDS = True

                if chekFileToASFK and chekFileToPUDS:
                    try:
                        os.remove(myFile)
                        self.log_str.emit(datetime.datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S") + ' Файл ' + file + ' удален из ' + fromBANKBuff)
                        chekArhive = False
                    except:
                        self.log_str.emit(datetime.datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S") + ' Не удалось удалить ' + file + ' из ' + fromBANKBuff)
                        chekArhive = False
            try:
                shutil.move(fromBANKBuff + '\\' + file, fromBANKBuff + '\\' + '1')
            except Exception:
                pass