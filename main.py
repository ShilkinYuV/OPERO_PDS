import sys

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt6.QtGui import QIcon

from AboutForm import AboutForm
from mainapp import Ui_MainWindow
from xml.dom import minidom
from EpdDay import EpdDay
from EpdNight import EpdNight
import os
import shutil
import datetime
import logging
import subprocess
from path_constants import fromASFK,fromPUDS,toBANK, logTo


class OperoPDS(QtWidgets.QMainWindow):
    log_str = QtCore.pyqtSignal(str)

    def __init__(self):
        super(OperoPDS, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        currentDate = datetime.datetime.now()
        self.isASFK = fromASFK + '\\' + currentDate.strftime("%Y%m%d")
        self.isASFKArhive = fromASFK + '\\' + str(1)
        self.isPUDS = fromPUDS + '\\' + currentDate.strftime("%Y%m%d")
        self.inBANK = toBANK
        self.LOGS = logTo
        self.OTVSEND = 'RDI0NCB4bWxucz0idXJuOmNici1ydTplZDp2Mi4wIiBFRE5vPSI'
        self.OTZVSEND = 'RDI3NSB4bWxucz0idXJuOmNici1ydTplZDp2Mi4wIiBFRE5vPSI'
        self.PESSEND = 'YWNrZXRFSUQgeG1sbnM9InVybjpjYnItcnU6ZWQ6djIuMCIgRURObz0i'
        self.RNPSEND = 'YWNrZXRFUEQgeG1sbnM9InVybjpjYnItcnU6ZWQ6djIuMCIgRURObz0i'
        self.ZINFSEND = 'RDI0MCBFREF1dGhvcj0i'
        self.ZONDSEND = 'RDk5OSBDcmVhdGlvbkRhdGVUaW1l'
        self.ZVPSEND = 'RDIxMCB4bWxucz0idXJuOmNici1ydTplZDp2Mi4wIiBFRE5vPSI'
        self.ui.chekDocuments.clicked.connect(self.checkfiles)
        self.ui.OTVSEND.clicked.connect(lambda: self.sending(self.OTVSEND))
        self.ui.OTZVSEND.clicked.connect(lambda: self.sending(self.OTZVSEND))
        self.ui.PESSEND.clicked.connect(lambda: self.sending(self.PESSEND))
        self.ui.RNPSEND.clicked.connect(lambda: self.sending(self.RNPSEND))
        self.ui.ZINFSEND.clicked.connect(lambda: self.sending(self.ZINFSEND))
        self.ui.ZONDSEND.clicked.connect(lambda: self.sending(self.ZONDSEND))
        self.ui.ZVPSEND.clicked.connect(lambda: self.sending(self.ZVPSEND))
        self.ui.pushButton_2.clicked.connect(self.open_about_form)
        self.ui.clearWindow.clicked.connect(self.clearWindow)
        self.chekdirs()
        logging.basicConfig(filename=logTo + '\\1\\' + currentDate.strftime("%Y%m%d") + '\\' + "sample.log", level=logging.INFO)
        self.epdDay = EpdDay(my_window=self)
        self.epdNight = EpdNight(my_window=self)
        self.epdNight.log_str.connect(self.logining)
        self.epdDay.log_str.connect(self.logining)
        self.log_str.connect(self.logining)

    @QtCore.pyqtSlot(str)
    def logining(self, str):
        self.ui.textEdit.append(str)
        logging.info(str)

        # обновление имен каталого в наименованием текущей даты
    def updateDates(self):
        currentDate = datetime.datetime.now()
        self.isASFK = fromASFK + '\\' + currentDate.strftime("%Y%m%d")
        self.isPUDS = fromPUDS + '\\' + currentDate.strftime("%Y%m%d")

    # Проверка существуют ли каталоги, если не существуют то каталоги создаются
    def chekdirs(self):
        self.updateDates()
        currentDate = datetime.datetime.now()
        if not os.path.exists(self.LOGS + '\\' + '1' + '\\' + currentDate.strftime("%Y%m%d")):
            os.makedirs(self.LOGS + '\\' + '1' + '\\' + currentDate.strftime("%Y%m%d"))
        if not os.path.exists(self.isASFK):
            os.makedirs(self.isASFK)
        if not os.path.exists(self.isPUDS):
            os.makedirs(self.isPUDS)
        if not os.path.exists(self.isASFKArhive + '\\' + currentDate.strftime("%Y%m%d")):
            os.makedirs(self.isASFKArhive + '\\' + currentDate.strftime("%Y%m%d"))

    def clearWindow(self):
        self.ui.textEdit.clear()

    #Копирование файлов из isASFK и isPUDS в зависимости от типа, логирование и вывод результата на экран
    def sending(self, type):
        chekArhive = False
        self.chekdirs()
        dirsASFKPUDS = [self.isASFK, self.isPUDS]
        isEmpty = True
        for currentdirs in dirsASFKPUDS:
            files = os.listdir(currentdirs)
            for file in files:
                myFile = currentdirs + '\\' + file
                mydoc = minidom.parse(myFile)
                items = mydoc.getElementsByTagName('sen:Object')
                for elem in items:
                    self.elementXML = str(elem.firstChild.data)
                    if self.elementXML.__contains__(type):
                        self.log_str.emit(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Начало копирования ' + file + ' в ' + self.inBANK)
                        isEmpty = False
                        try:
                            shutil.copy2(myFile, self.isASFKArhive + '\\' + datetime.datetime.now().strftime("%Y%m%d"))
                            self.log_str.emit(datetime.datetime.now().strftime(
                                "%Y-%m-%d %H:%M:%S") + ' Копирование ' + file + ' из ' + currentdirs + ' в ' + (self.isASFKArhive + '\\' + datetime.datetime.now().strftime("%Y%m%d")) + ' успешно завершено')
                        except Exception:
                            self.log_str.emit(datetime.datetime.now().strftime(
                                "%Y-%m-%d %H:%M:%S") + ' Копирование ' + file + ' из ' + currentdirs + ' в ' + (self.isASFKArhive + '\\' + datetime.datetime.now().strftime("%Y%m%d")) + ' не удалось')
                        try:
                            shutil.copy2(myFile, self.inBANK)
                            self.log_str.emit(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Копирование ' + file + ' из ' + currentdirs + ' в ' + self.inBANK + ' успешно завершено')
                        except Exception:
                            self.log_str.emit(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Копирование ' + file + ' из ' + currentdirs + ' в ' + self.inBANK + ' не удалось')

                        arhivefiles = os.listdir(self.isASFKArhive + '\\' + datetime.datetime.now().strftime("%Y%m%d"))
                        for arhive in arhivefiles:
                            if arhive.__contains__(file):
                                self.log_str.emit(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Файл ' + file + ' присутствует в ' + (self.isASFKArhive + '\\' + datetime.datetime.now().strftime("%Y%m%d")))
                                chekArhive = True

                        bankfiles = os.listdir(self.inBANK)
                        for bankfile in bankfiles:
                            if bankfile.__contains__(file) and chekArhive:
                                self.log_str.emit(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Файл ' + file + ' присутствует в ' + self.inBANK)
                                try:
                                    os.remove(myFile)
                                    self.log_str.emit(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Файл ' + file + ' удален из ' + currentdirs)
                                    chekArhive = False
                                except:
                                    self.log_str.emit(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Не удалось удалить ' + file + ' из ' + currentdirs)
                                    chekArhive = False

        if isEmpty:
            sender = self.sender()
            self.log_str.emit(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Корневые каталоги не содержат файлов ' + sender.text())

    # Метод проверяет наличие файлов в каталогах isASFK и isPuds, результат выводит на экран
    def checkfiles(self):
        self.chekdirs()
        dirsASFKPUDS = [self.isASFK, self.isPUDS]
        isEmpty = True
        for currentdirs in dirsASFKPUDS:
            files = os.listdir(currentdirs)

            for file in files:
                myFile = currentdirs + '\\' + file
                mydoc = minidom.parse(myFile)
                items = mydoc.getElementsByTagName('sen:Object')

                for elem in items:
                    self.elementXML = str(elem.firstChild.data)
                    if self.elementXML.__contains__(self.OTVSEND):
                        self.ui.textEdit.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' OTVSEND ' + file)
                        isEmpty = False
                    elif self.elementXML.__contains__(self.OTVSEND):
                        self.ui.textEdit.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' OTZVSEND ' + file)
                        isEmpty = False
                    elif self.elementXML.__contains__(self.PESSEND):
                        self.ui.textEdit.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' PESSEND ' + file)
                        isEmpty = False
                    elif self.elementXML.__contains__(self.RNPSEND):
                        self.ui.textEdit.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' RNPSEND ' + file)
                        isEmpty = False
                    elif self.elementXML.__contains__(self.ZINFSEND):
                        self.ui.textEdit.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' ZINFSEND ' + file)
                        isEmpty = False
                    elif self.elementXML.__contains__(self.ZONDSEND):
                        self.ui.textEdit.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' ZONDSEND ' + file)
                        isEmpty = False
                    elif self.elementXML.__contains__(self.ZVPSEND):
                        self.ui.textEdit.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' ZVPSEND ' + file)
                        isEmpty = False

        if isEmpty:
            self.ui.textEdit.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Корневые каталоги не содержат файлов')

    def open_about_form(self):
        self.about_form = AboutForm()
        self.about_form.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = OperoPDS()
    application.show()

    sys.exit(app.exec())
