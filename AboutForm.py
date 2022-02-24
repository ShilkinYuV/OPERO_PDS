
from AboutWindow import Ui_aboutWindow
from PyQt5 import QtWidgets
import constants


class AboutForm(QtWidgets.QWidget):
    def __init__(self):
        super(AboutForm, self).__init__()
        self.ui = Ui_aboutWindow()
        self.ui.setupUi(self)
        self.ui.poLabel.setText(constants.app_name)
        self.ui.versionLabel.setText(self.ui.versionLabel.text() + constants.app_version)
        self.setFixedSize(self.size())