import sys

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt6.QtGui import QIcon
from mainapp import Ui_MainWindow
from xml.dom import minidom
import os
import shutil


class OperoPDS(QtWidgets.QMainWindow):

    def __init__(self):
        super(OperoPDS, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.isASFK = 'D:\\isASFK'
        self.isPUDS = 'D:\\isPUDS'
        self.inBANK = 'D:\\OEV\\Exg\\cli'
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

    def sending(self, type):
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
                        self.ui.textEdit.append('       Начало копирования ' + file + ' в ' + self.inBANK)
                        isEmpty = False
                        try:
                            shutil.copy2(myFile, self.inBANK + '\\' + file)
                            self.ui.textEdit.append('Копирование ' + file + ' из ' + currentdirs +' в ' + self.inBANK + ' успешно завершено')
                        except Exception:
                            self.ui.textEdit.append('Копирование ' + file + ' из ' + currentdirs + ' в ' + self.inBANK + ' не удалось')

                        bankfiles = os.listdir(self.inBANK)
                        for bankfile in bankfiles:
                            if bankfile.__contains__(file):
                                self.ui.textEdit.append('Файл ' + file + ' присутствует в ' + self.inBANK)
                                try:
                                    os.remove(myFile)
                                    self.ui.textEdit.append('Файл ' + file + ' удален из ' + currentdirs)
                                except:
                                    self.ui.textEdit.append('Не удалось удалить ' + file + ' из ' + currentdirs)

        if isEmpty:
            sender = self.sender()
            self.ui.textEdit.append('Корневые каталоги не содержат файлов ' + sender.text())

    def checkfiles(self):
        dirsASFKPUDS = [self.isASFK, self.isPUDS]

        for currentdirs in dirsASFKPUDS:
            files = os.listdir(currentdirs)
            print(files)

            for file in files:
                myFile = currentdirs + '\\' + file
                mydoc = minidom.parse(myFile)
                items = mydoc.getElementsByTagName('sen:Object')

                for elem in items:
                    self.elementXML = str(elem.firstChild.data)
                    if self.elementXML.__contains__(self.OTVSEND):
                        print('OTVSEND ' + file)
                        self.ui.textEdit.append('OTVSEND ' + file)
                    elif self.elementXML.__contains__(self.OTVSEND):
                        print('OTZVSEND ' + file)
                        self.ui.textEdit.append('OTZVSEND ' + file)
                    elif self.elementXML.__contains__(self.PESSEND):
                        print('PESSEND ' + file)
                        self.ui.textEdit.append('PESSEND ' + file)
                    elif self.elementXML.__contains__(self.RNPSEND):
                        print('RNPSEND ' + file)
                        self.ui.textEdit.append('RNPSEND ' + file)
                    elif self.elementXML.__contains__(self.ZINFSEND):
                        print('ZINFSEND ' + file)
                        self.ui.textEdit.append('ZINFSEND ' + file)
                    elif self.elementXML.__contains__(self.ZONDSEND):
                        print('ZONDSEND ' + file)
                        self.ui.textEdit.append('ZONDSEND ' + file)
                    elif self.elementXML.__contains__(self.ZVPSEND):
                        print('ZVPSEND ' + file)
                        self.ui.textEdit.append('ZVPSEND ' + file)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = OperoPDS()
    application.show()

    sys.exit(app.exec())
