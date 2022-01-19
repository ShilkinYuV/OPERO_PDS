import sys

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt6.QtGui import QIcon
from mainapp import Ui_MainWindow


class OperoPDS(QtWidgets.QMainWindow):

    def __init__(self):
        super(OperoPDS, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = OperoPDS()
    application.show()

    sys.exit(app.exec())

