from xml.dom import minidom
from PyQt5 import QtWidgets, QtCore, QtGui
from ui_forms.MainWindow import Ui_MainWindow
from forms.AboutForm import AboutForm
import os

from datetime import datetime
from contants.path_constants import (
    dir_log,
    dir_armkbr,
    dir_archive,
    arm_buf,
    unb64_rabis,
    trans_disk,
    puds_disk,
    CLI
)
from libs.FileExplorer import FileExplorer
from libs.Logger import Logger


class MainForm(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super(MainForm, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.textEdit.setReadOnly(True)
        self.ui.day.clicked.connect(self.epd_day_start)
        
        self.OTVSEND = 'RDI0NCB4bWxucz0idXJuOmNici1ydTplZDp2Mi4wIiBFRE5vPSI'
        self.OTZVSEND = 'RDI3NSB4bWxucz0idXJuOmNici1ydTplZDp2Mi4wIiBFRE5vPSI'
        self.PESSEND = 'YWNrZXRFSUQgeG1sbnM9InVybjpjYnItcnU6ZWQ6djIuMCIgRURObz0i'
        self.RNPSEND = 'YWNrZXRFUEQgeG1sbnM9InVybjpjYnItcnU6ZWQ6djIuMCIgRURObz0i'
        self.ZINFSEND = 'RDI0MCBFREF1dGhvcj0i'
        self.ZONDSEND = 'RDk5OSBDcmVhdGlvbkRhdGVUaW1l'
        self.ZVPSEND = 'RDIxMCB4bWxucz0idXJuOmNici1ydTplZDp2Mi4wIiBFRE5vPSI'

        self.ui.OTVSEND.clicked.connect(lambda: self.send_docs(self.OTVSEND))
        self.ui.OTZVSEND.clicked.connect(lambda: self.send_docs(self.OTZVSEND))
        self.ui.PESSEND.clicked.connect(lambda: self.send_docs(self.PESSEND))
        self.ui.RNPSEND.clicked.connect(lambda: self.send_docs(self.RNPSEND))
        self.ui.ZINFSEND.clicked.connect(lambda: self.send_docs(self.ZINFSEND))
        self.ui.ZONDSEND.clicked.connect(lambda: self.send_docs(self.ZONDSEND))
        self.ui.ZVPSEND.clicked.connect(lambda: self.send_docs(self.ZVPSEND))

        self.about_form = None
        self.ui.pushButton_2.clicked.connect(self.open_about_form)

        self.logger = Logger(form_log_path=self.ui.textEdit)

    def open_about_form(self):
        self.about_form = AboutForm()
        self.about_form.show()

    def epd_day_start(self):

        file_explorer = FileExplorer(_logger=self.logger)
        file_explorer.check_dir(dir_log)
        file_explorer.check_dir(dir_armkbr + "\\exg\\rcv")

        current_date = datetime.now().strftime("%d.%m.%Y")

        if file_explorer.count_files_in_folder(dir_armkbr + "\\exg\\rcv") == 0:
            print("Нет файлов по директории арм кбрн")

        else:
            file_explorer.check_dir(dir_archive)
            file_explorer.check_dir(arm_buf)

            file_explorer.move_files(dir_armkbr + "\\exg\\rcv", arm_buf)
            
            file_explorer.decode_files(unb64_rabis,arm_buf,dir_log)

            arc_dir = dir_archive + "\\" + current_date + "\\uarm3\\inc\\ed"

            file_explorer.check_dir(arc_dir)

            file_explorer.copy_files(arm_buf, arc_dir, r".*\.ed\.xml")
            file_explorer.copy_files(arm_buf, arc_dir, r".*ed211.*\.ed\.xml")

            trans_disk_path = trans_disk + "IN_OEBS_BIK\\044525000"

            file_explorer.copy_files(arm_buf, trans_disk_path, r".*\.ed\.xml")
            file_explorer.copy_files(arm_buf, trans_disk_path, r".*ed211.*\.ed\.xml")

            file_explorer.copy_files(arm_buf, puds_disk + "input", r".*\.ed")
            file_explorer.copy_files(arm_buf, puds_disk + "input", r".*ed211.*\.eds")

            file_explorer.delete_files(arm_buf, r".*\.xml")

            file_explorer.copy_files(arm_buf, dir_armkbr + "\\exg\\rcv\\1")

            file_explorer.delete_files(arm_buf)


    def send_docs(self, rnp):
        
        file_explorer = FileExplorer(_logger=self.logger)

        current_date = datetime.now().strftime("%d%m%Y")

        vchera = trans_disk + "\\OUT_OEBS\\4800\\044525000\\" + current_date
        odin = vchera + "\\1"

        file_explorer.check_dir(vchera)
        file_explorer.check_dir(odin)

        vcheran = trans_disk + "\\OUT_OEBS\\4800\\004525987\\" + current_date
        odinn = vcheran + "\\1"

        file_explorer.check_dir(vcheran)
        file_explorer.check_dir(odinn)
              
        count = 0      

        for file_name in os.listdir(vchera):
            file_path = vchera + "\\" + file_name
            if os.path.isfile(file_path):
                    mydoc = minidom.parse(file_path)
                    items = mydoc.getElementsByTagName('sen:Object')
                    for elem in items:
                        self.elementXML = str(elem.firstChild.data)
                        if self.elementXML.__contains__(rnp):
                            file_explorer.copy_files(vchera, odin, filter=file_name.lower())
                            count+=1

        for file_name in os.listdir(vcheran):
            file_path = vcheran + "\\" + file_name
            if os.path.isfile(file_path):
                    mydoc = minidom.parse(file_path)
                    items = mydoc.getElementsByTagName('sen:Object')
                    for elem in items:
                        self.elementXML = str(elem.firstChild.data)
                        if self.elementXML.__contains__(rnp):
                            file_explorer.copy_files(vcheran, odinn, filter=file_name.lower())
                            count+=1

        if count == 0:
            sender = self.sender()
            self.logger.log("Не найдено ни одного документа {}".format(sender.text()))
        