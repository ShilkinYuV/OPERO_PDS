import sys

from PyQt5 import QtWidgets, QtCore, QtGui
import ctypes, sys

from AboutForm import AboutForm
from mainapp import Ui_MainWindow
from xml.dom import minidom
from EpdDay import EpdDay
from EpdNight import EpdNight
import os
import shutil
import datetime
import logging
from CheckConnection import CheckConnection
from path_constants import fromASFK, fromPUDS, toBANK, logTo


class OperoPDS(QtWidgets.QMainWindow):
    log_str = QtCore.pyqtSignal(str, bool)

    def __init__(self):
        super(OperoPDS, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # self.mapping_network_drives()
        self.ui.textEdit.setReadOnly(True)
        currentDate = datetime.datetime.now()
        self.isASFK = fromASFK + '\\' + currentDate.strftime("%d%m%Y")
        self.isASFKArhive = self.isASFK + '\\' + str(1)
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
        self.checkConnection = CheckConnection()
        self.checkConnection.setDaemon(True)
        self.checkConnection.start()

    def mapping_network_drives(self):
        os.system('set trans_disk=x:')
        os.system('set puds_disk=w:')
        os.system('net use %trans_disk% /delete /y')
        os.system('net use %puds_disk% /delete /y')
        os.system('net use x: \\\\10.48.4.241\\transportbanks 1!QQww /USER:10.48.4.241\\svc95004800')
        os.system('net use w: \\\\10.48.4.241\\transport 1!QQww /USER:10.48.4.241\\svc95004800')

    # ?????????? ???????????????????? ???? ?????????? ?? ??????????????????????
    @QtCore.pyqtSlot(str, bool)
    def logining(self, text, type):
        if type:
            logging.info(text)
        else: 
            logging.error(text)

        text = text.replace('|', '')
        text = text.replace(text[19:26],'')

        self.ui.textEdit.append(text)

        # ???????????????????? ???????? ???????????????? ?? ?????????????????????????? ?????????????? ????????
    def updateDates(self):
        currentDate = datetime.datetime.now()
        self.isASFK = fromASFK + '\\' + currentDate.strftime("%d%m%Y")
        self.isPUDS = fromPUDS + '\\' + currentDate.strftime("%Y%m%d")
        self.isASFKArhive = self.isASFK + '\\' + str(1)

    # ???????????????? ???????????????????? ???? ????????????????, ???????? ???? ???????????????????? ???? ???????????????? ??????????????????
    def chekdirs(self):
        self.updateDates()
        currentDate = datetime.datetime.now()
        if not os.path.exists(self.LOGS + '\\' + '1' + '\\' + currentDate.strftime("%Y%m%d")):
            os.makedirs(self.LOGS + '\\' + '1' + '\\' + currentDate.strftime("%Y%m%d"))
        if not os.path.exists(self.isASFK):
            os.makedirs(self.isASFK)
        if not os.path.exists(self.isPUDS):
            os.makedirs(self.isPUDS)
        if not os.path.exists(self.isASFKArhive):
            os.makedirs(self.isASFKArhive)

    def clearWindow(self):
        self.ui.textEdit.clear()

    #?????????????????????? ???????????? ???? isASFK ?? isPUDS ?? ?????????????????????? ???? ????????, ?????????????????????? ?? ?????????? ???????????????????? ???? ??????????
    def sending(self, type):
        chekArhive = False
        self.chekdirs()
        dirsASFKPUDS = [self.isASFK, self.isPUDS]
        isEmpty = True
        for currentdirs in dirsASFKPUDS:
            files = os.listdir(currentdirs)
            for file in files:
                myFile = currentdirs + '\\' + file
                if os.path.isfile(myFile):
                    mydoc = minidom.parse(myFile)
                    items = mydoc.getElementsByTagName('sen:Object')
                    for elem in items:
                        self.elementXML = str(elem.firstChild.data)
                        if self.elementXML.__contains__(type):
                            self.log_str.emit('|'+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + '| ???????????? ?????????????????????? ' + file + ' ?? ' + self.inBANK, True)
                            isEmpty = False
                            try:
                                shutil.copy2(myFile, self.isASFKArhive)
                                self.log_str.emit('|'+datetime.datetime.now().strftime(
                                    "%Y-%m-%d %H:%M:%S.%f") + '| ?????????????????????? ' + file + ' ???? ' + currentdirs + ' ?? ' + (self.isASFKArhive ) + ' ?????????????? ??????????????????', True)
                            except Exception:
                                self.log_str.emit('|'+datetime.datetime.now().strftime(
                                    "%Y-%m-%d %H:%M:%S.%f") + '| ?????????????????????? ' + file + ' ???? ' + currentdirs + ' ?? ' + (self.isASFKArhive) + ' ???? ??????????????', False)
                            try:
                                shutil.copy2(myFile, self.inBANK)
                                self.log_str.emit('|'+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + '| ?????????????????????? ' + file + ' ???? ' + currentdirs + ' ?? ' + self.inBANK + ' ?????????????? ??????????????????', True)
                            except Exception:
                                self.log_str.emit('|'+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + '| ?????????????????????? ' + file + ' ???? ' + currentdirs + ' ?? ' + self.inBANK + ' ???? ??????????????', False)

                            arhivefiles = os.listdir(self.isASFKArhive)
                            for arhive in arhivefiles:
                                myArhiveFile = self.isASFKArhive + '\\' + arhive
                                if os.path.isfile(myArhiveFile):
                                    if arhive.__contains__(file):
                                        self.log_str.emit('|'+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + '| ???????? ' + file + ' ???????????????????????? ?? ' + (self.isASFKArhive), True)
                                        chekArhive = True

                            bankfiles = os.listdir(self.inBANK)
                            for bankfile in bankfiles:
                                MyBankFile = self.inBANK + '\\' + bankfile
                                if os.path.isfile(MyBankFile):
                                    if bankfile.__contains__(file) and chekArhive:
                                        self.log_str.emit('|'+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + '| ???????? ' + file + ' ???????????????????????? ?? ' + self.inBANK, True)
                                        try:
                                            os.remove(myFile)
                                            self.log_str.emit('|'+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + '| ???????? ' + file + ' ???????????? ???? ' + currentdirs, True)
                                            chekArhive = False
                                        except:
                                            self.log_str.emit('|'+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + '| ???? ?????????????? ?????????????? ' + file + ' ???? ' + currentdirs, False)
                                            chekArhive = False

        if isEmpty:
            sender = self.sender()
            self.log_str.emit('|'+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + '| ???????????????? ???????????????? ???? ???????????????? ???????????? ' + sender.text(), True)

    # ?????????? ?????????????????? ?????????????? ???????????? ?? ?????????????????? isASFK ?? isPuds, ?????????????????? ?????????????? ???? ??????????
    def checkfiles(self):
        self.chekdirs()
        dirsASFKPUDS = [self.isASFK, self.isPUDS]
        isEmpty = True
        for currentdirs in dirsASFKPUDS:
            files = os.listdir(currentdirs)
            for file in files:
                myFile = currentdirs + '\\' + file
                if os.path.isfile(myFile):
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
            self.ui.textEdit.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' ???????????????? ???????????????? ???? ???????????????? ????????????')

    def open_about_form(self):
        self.about_form = AboutForm()
        self.about_form.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = OperoPDS()
    application.show()    
    sys.exit(app.exec())

