from PyQt5 import QtWidgets
import sys
from forms.MainForm import MainForm

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = MainForm()
    application.show()
    sys.exit(app.exec())
