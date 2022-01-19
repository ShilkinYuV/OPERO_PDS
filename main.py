import sys

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt6.QtGui import QIcon
from mainapp import Ui_MainWindow
from xml.dom import minidom
import os


class OperoPDS(QtWidgets.QMainWindow):

    def __init__(self):
        super(OperoPDS, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.isASFK = 'D:\\isASFK'
        self.isPUDS = 'D:\\isPUDS'
        self.OTVSEND = 'RDI0NCB4bWxucz0idXJuOmNici1ydTplZDp2Mi4wIiBFRE5vPSI'
        self.OTZVSEND = 'RDI3NSB4bWxucz0idXJuOmNici1ydTplZDp2Mi4wIiBFRE5vPSI'
        self.PESSEND = 'YWNrZXRFSUQgeG1sbnM9InVybjpjYnItcnU6ZWQ6djIuMCIgRURObz0i'
        self.RNPSEND = 'YWNrZXRFUEQgeG1sbnM9InVybjpjYnItcnU6ZWQ6djIuMCIgRURObz0i'
        self.ZINFSEND = 'RDI0MCBFREF1dGhvcj0i'
        self.ZONDSEND = 'RDk5OSBDcmVhdGlvbkRhdGVUaW1l'
        self.ZVPSEND = 'RDIxMCB4bWxucz0idXJuOmNici1ydTplZDp2Mi4wIiBFRE5vPSI'

        files = os.listdir(self.isASFK)
        print(files)

        for file in files:
            myFile = self.isASFK + '\\' + file
            mydoc = minidom.parse(myFile)
            items = mydoc.getElementsByTagName('sen:Object')

            for elem in items:
                self.elementXML = str(elem.firstChild.data)
                if self.elementXML.__contains__(self.OTVSEND):
                    print('OTVSEND ' + myFile)
                elif self.elementXML.__contains__(self.OTVSEND):
                    print('OTZVSEND' + myFile)
                elif self.elementXML.__contains__(self.PESSEND):
                    print('PESSEND' + myFile)
                elif self.elementXML.__contains__(self.RNPSEND):
                    print('RNPSEND' + myFile)
                elif self.elementXML.__contains__(self.ZINFSEND):
                    print('ZINFSEND' + myFile)
                elif self.elementXML.__contains__(self.ZONDSEND):
                    print('ZONDSEND' + myFile)
                elif self.elementXML.__contains__(self.ZVPSEND):
                    print('ZVPSEND' + myFile)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = OperoPDS()
    application.show()

    sys.exit(app.exec())

