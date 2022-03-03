from datetime import datetime
import os
from re import L
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


class CheckDirs(QThread):

    log_str = QtCore.pyqtSignal(str, bool, bool)

    def __init__(self, form, doc_types):
        QThread.__init__(self)
        self.form = form
        self.fe = FileExplorer()
        self.doc_types = doc_types
        self.fe.log_str.connect(form.log)

    def run(self):
        """Проверка наличия документов для отправки"""

        current_date = datetime.now().strftime("%d%m%Y")

        vchera = trans_disk + "\\OUT_OEBS\\4800\\044525000\\" + current_date
        vcheran = trans_disk + "\\OUT_OEBS\\4800\\004525987\\" + current_date

        current_date = datetime.now().strftime("%Y%m%d")
        puds_dir = puds_disk + '\\output\\' + current_date

        rnp_folders={vchera: "АСФК", vcheran: "АСФК", puds_dir: "ПУДС"}

        isEmpty = True

        for folder, doc_from in rnp_folders.items():
            count_doc_types = {k:0 for k,v in self.doc_types.items()}
            self.fe.check_dir(folder)
            for file_name in os.listdir(folder):
                file_path = folder + "\\" + file_name
                if os.path.isfile(file_path):
                    mydoc = minidom.parse(file_path)
                    items = mydoc.getElementsByTagName("sen:Object")
                    for elem in items:
                        self.elementXML = str(elem.firstChild.data)
                        for k,v in self.doc_types.items():
                            if self.elementXML.__contains__(v):
                                isEmpty = False
                                count_doc_types[k] += 1

            for k,v in count_doc_types.items():
                if v != 0:
                    self.log_str.emit(
                            "Найдены документы для отправки типа - {}, в количестве {} из {}".format(k, v, doc_from), False, False
                        )    

        [count, confirm_count] = self.fe.count_files_in_folder(dir_armkbr + "\\exg\\rcv")
        

        if count != 0:
            isEmpty = False
            self.log_str.emit("Найдены документы для загрузки ЭПД в количестве {}".format(count), False, False)

        if confirm_count != 0:
            self.log_str.emit("Найдены квитки по директории ЭПД в количестве {}".format(confirm_count), False, False)

        if isEmpty:
            self.log_str.emit("Документов для загрузки не найдено", False, False)