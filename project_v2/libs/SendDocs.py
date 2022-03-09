from datetime import datetime
import os
from xml.dom import minidom
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
from libs.LogType import LogType


class SendDocs(QThread):

    log_str = QtCore.pyqtSignal(str,LogType)

    def __init__(self, form, button, rnp, doc_type, isFromPuds):
        QThread.__init__(self)
        self.form = form
        self.fe = FileExplorer()
        self.fe.log_str.connect(form.log)
        self.rnp = rnp
        self.doc_type = doc_type
        self.isFromPuds = isFromPuds
        self.button = button

    def run(self):
        """Отправка определенных документов выбираемых на RNP"""
        self.button.setDisabled(True)
        count = 0
        if self.isFromPuds is False:
            current_date = datetime.now().strftime("%d%m%Y")
            vchera = trans_disk + "\\OUT_OEBS\\4800\\044525000\\" + current_date

            self.fe.check_dir(vchera)

            vcheran = trans_disk + "\\OUT_OEBS\\4800\\004525987\\" + current_date

            self.fe.check_dir(vcheran)

            count += self.send_docs(rnp=self.rnp, path_from=vchera, path_to=CLI)
            count += self.send_docs(rnp=self.rnp, path_from=vcheran, path_to=CLI)
        else:
            current_date = datetime.now().strftime("%Y%m%d")
            dir = puds_disk + '\\output\\' + current_date

            self.fe.check_dir(dir)

            count+=self.send_docs(rnp=self.rnp, path_from=dir, path_to=CLI)

        if count == 0:
            self.log_str.emit(
                "Не отправлено ни одного документа {}".format(self.doc_type), LogType.INFO
            )
        else:
            self.log_str.emit(
                "Отправлено {} документов {}".format(count, self.doc_type), LogType.INFO
            )

        self.button.setDisabled(False)

    def send_docs(self, rnp, path_from, path_to):

        archive = path_from + "\\1"
        self.fe.check_dir(archive)
        self.fe.check_dir(path_to)

        count = 0
        for file_name in os.listdir(path_from):
            file_path = path_from + "\\" + file_name
            if os.path.isfile(file_path):
                if os.path.exists(archive + "\\" + file_name) == False: # Проверка на наличие в архиве
                    if os.path.exists(path_to + "\\" + file_name) == False: # Проверка на наличие на транспортном диске
                        mydoc = minidom.parse(file_path)
                        items = mydoc.getElementsByTagName("sen:Object")
                        for elem in items:
                            self.elementXML = str(elem.firstChild.data)
                            if self.elementXML.__contains__(rnp):
                                self.fe.copy_files(path_from, path_to, filter=file_name.lower())
                                self.fe.move_files(path_from, archive, filter=file_name.lower())
                                count += 1
                    else:
                        self.log_str.emit("Документ {} уже присутствует на транспортном диске {}".format(file_name, path_to), LogType.WARNING)
                else:
                    self.log_str.emit("Документ {} уже присутствует в архиве {}".format(file_name, archive), LogType.WARNING)


        return count