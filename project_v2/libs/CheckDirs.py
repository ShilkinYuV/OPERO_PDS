from datetime import datetime
from PyQt5.QtCore import QThread
from PyQt5 import QtCore, QtWidgets, QtGui

# import time

from contants.path_constants import (
    dir_log,
    dir_armkbr,
    dir_archive,
    arm_buf,
    unb64_rabis,
    trans_disk,
    puds_disk,
    CLI,
)

from libs.FileExplorer import FileExplorer


class CheckDirs(QThread):

    log_str = QtCore.pyqtSignal(str, bool, bool)

    def __init__(self, form, doc_types):
        QThread.__init__(self)
        self.form = form
        self.fe = FileExplorer()
        self.doc_types = doc_types
        self.fe.log_str.connect(form.log)

    def run(self):
        """Отправка определенных документов выбираемых на RNP"""

        current_date = datetime.now().strftime("%d%m%Y")

        vchera = trans_disk + "\\OUT_OEBS\\4800\\044525000\\" + current_date
        vcheran = trans_disk + "\\OUT_OEBS\\4800\\004525987\\" + current_date

        self.fe.check_dirs_for_send_docs(
            rnp_folders=[vchera, vcheran],
            rnp_doc_types=self.doc_types,
            dir_armkbrn=(dir_armkbr + "\\exg\\rcv"),
        )
        