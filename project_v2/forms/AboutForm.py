
from ui_forms.AboutWindow import Ui_aboutWindow
from PyQt5 import QtWidgets
from contants import app_constants


class AboutForm(QtWidgets.QWidget):
    def __init__(self):
        super(AboutForm, self).__init__()
        self.ui = Ui_aboutWindow()
        self.ui.setupUi(self)
        self.ui.poLabel.setText(app_constants.app_name)
        self.ui.versionLabel.setText(self.ui.versionLabel.text() + app_constants.app_version)
        self.setFixedSize(self.size())