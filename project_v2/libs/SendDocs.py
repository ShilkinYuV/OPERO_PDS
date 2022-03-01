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


class SendDocs(QThread):

    log_str = QtCore.pyqtSignal(str, bool, bool)

    def __init__(self, form, rnp, doc_type):
        QThread.__init__(self)
        self.form = form
        self.fe = FileExplorer()
        self.fe.log_str.connect(form.log)
        self.rnp = rnp
        self.doc_type = doc_type

    def run(self):
        """Отправка определенных документов выбираемых на RNP"""
        current_date = datetime.now().strftime("%d%m%Y")

        vchera = trans_disk + "\\OUT_OEBS\\4800\\044525000\\" + current_date

        self.fe.check_dir(vchera)

        vcheran = trans_disk + "\\OUT_OEBS\\4800\\004525987\\" + current_date

        self.fe.check_dir(vcheran)

        count = 0

        count += self.fe.check_dir_for_docs(
            rnp=self.rnp, path_from=vchera, path_to=CLI
        )
        count += self.fe.check_dir_for_docs(
            rnp=self.rnp, path_from=vcheran, path_to=CLI
        )

        if count == 0:
            self.log_str.emit("Не найдено ни одного документа {}".format(self.doc_type), False, False)
        