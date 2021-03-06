from datetime import datetime
from PyQt5.QtCore import QThread
from PyQt5 import QtCore
import os

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


class NightCicle(QThread):

    log_str = QtCore.pyqtSignal(str, LogType)
    update_counts = QtCore.pyqtSignal(int, int)

    def __init__(self,form):
        QThread.__init__(self)
        self.work = True
        self.fe = FileExplorer()
        self.fe.log_str.connect(form.log)

    def mapping_network_drives(self):
        os.system("set trans_disk=x:")
        os.system("set puds_disk=w:")
        os.system("net use %trans_disk% /delete /y")
        os.system("net use %puds_disk% /delete /y")
        os.system(
            "net use x: \\\\10.48.4.241\\transportbanks 1!QQww /USER:10.48.4.241\\svc95004800"
        )
        os.system(
            "net use w: \\\\10.48.4.241\\transport 1!QQww /USER:10.48.4.241\\svc95004800"
        )

    def run(self):
        while self.work:
            
            time_now = datetime.time(datetime.now())
            time_to = datetime.time(datetime.strptime("09:00:00","%H:%M:%S"))
            time_from = datetime.time(datetime.strptime("20:30:00","%H:%M:%S"))
            time_between_1 = datetime.time(datetime.strptime("23:59:59","%H:%M:%S"))
            time_between_2 = datetime.time(datetime.strptime("00:00:00","%H:%M:%S"))
            # C 20:30 до 9 00 
            if time_now >= time_from and time_now <= time_between_1 or time_now >= time_between_2 and time_now <= time_to:
                self.mapping_network_drives()
                self.log_str.emit('', LogType.SPACE)
                self.fe.check_dir(dir_log)
                self.fe.check_dir(dir_armkbr + "\\exg\\rcv")

                current_date = datetime.now().strftime("%d.%m.%Y")

                if self.fe.count_files_in_folder(dir_armkbr + "\\exg\\rcv") == 0:
                    self.log_str.emit("Нет файлов к отправке!", LogType.INFO)

                else:
                    self.fe.check_dir(dir_archive)
                    self.fe.check_dir(arm_buf)

                    err, count, docs = self.fe.move_confirms(dir_armkbr + "\\exg\\rcv", dir_armkbr + "\\exg\\rcv\\1") # Исключить квитки без расширения
                    if not err and count!=0:
                        self.log_str.emit("Квитки успешно перемещены в архив в количестве {}".format(count), LogType.INFO)
                        # for doc in docs:
                        #     self.log_str.emit(doc, LogType.FILES)
                    elif not err and count == 0:
                        self.log_str.emit("Нет квитков для перемещения", LogType.INFO)

                    err, count, docs = self.fe.move_files(dir_armkbr + "\\exg\\rcv", arm_buf)
                    if not err and count != 0:
                        self.log_str.emit("Файлы успешно перемещены в буфер в кол-ве {}".format(count), LogType.INFO)
                        # for doc in docs:
                        #     self.log_str.emit(doc, LogType.FILES)
                    elif not err and count ==0:
                        self.log_str.emit("Нет файлов для перемещения в буфер", LogType.INFO)


                    self.fe.decode_files(unb64_rabis, arm_buf, dir_log)

                    arc_dir = dir_archive + "\\" + current_date + "\\uarm3\\inc\\ed"

                    self.fe.check_dir(arc_dir)


                    arc_xml_count = 0
                    arc_doc_list = []
                    err, count, docs = self.fe.copy_files(arm_buf, arc_dir, r".*\.ed\.xml$", name_of_doc='ed.xml')
                    if not err:
                        arc_xml_count+=count
                        arc_doc_list+=docs

                    err, count, docs = self.fe.copy_files(arm_buf, arc_dir, r".*ed211.*\.eds\.xml$", name_of_doc='ed211.eds.xml')
                    if not err:
                        arc_xml_count+=count
                        arc_doc_list+=docs

                    if arc_xml_count != 0:
                        self.log_str.emit("xml успешно скопированы в архив в кол-ве {} в {}".format(arc_xml_count, arc_dir), LogType.INFO)
                        # for doc in arc_doc_list:
                        #     self.log_str.emit(doc, LogType.FILES)
                    else:
                        self.log_str.emit("Нет документов xml для перемещения в архив.", LogType.INFO)

                    trans_disk_path = trans_disk + "IN_OEBS_BIK\\044525000"

                    xml_to_trans_disk_count = 0
                    xml_to_trans_disk_list = []
                    err, count, docs = self.fe.copy_files(arm_buf, trans_disk_path, r".*\.ed\.xml$", name_of_doc='ed.xml', default_check=False)
                    if not err:
                        xml_to_trans_disk_count+=count
                        xml_to_trans_disk_list+=docs
                    err, count, docs = self.fe.copy_files(arm_buf, trans_disk_path, r".*ed211.*\.eds\.xml$", name_of_doc='ed211.eds.xml', default_check=False)
                    if not err:
                        xml_to_trans_disk_count+=count
                        xml_to_trans_disk_list+=docs

                    if xml_to_trans_disk_count != 0:
                        self.log_str.emit("xml успешно скопированы на транспортный диск в кол-ве {}".format(xml_to_trans_disk_count), LogType.INFO)
                        for doc in xml_to_trans_disk_list:
                            self.log_str.emit(doc, LogType.FILES)
                        

                        self.update_counts.emit(0, xml_to_trans_disk_count)
                    else:
                        self.log_str.emit("Нет документов xml для перемещения в архив.", LogType.INFO)



                    ed_count = 0
                    ed_list = []
                    err, count, docs = self.fe.copy_files(arm_buf, puds_disk + "input", r".*\.ed$", name_of_doc='.eds', default_check=False)
                    if not err:
                        ed_count+=count
                        ed_list+=docs
                    err, count, docs = self.fe.copy_files(arm_buf, puds_disk + "input", r".*ed211.*\.eds$", name_of_doc='ed211.eds', default_check=False)
                    if not err:
                        ed_count+=count
                        ed_list+=docs

                    if ed_count!=0:
                        self.log_str.emit("ed успешно скопированы в кол-ве {} на диск ПУДС".format(ed_count),LogType.INFO)
                        for doc in ed_list:
                            self.log_str.emit(doc, LogType.FILES)
                    else:
                        self.log_str.emit("Нет документов ed для перемещения на диск ПУДС.", LogType.INFO)


                    self.fe.delete_files(arm_buf, r".*\.xml$", name_of_doc='.xml')

                    err, count, docs = self.fe.copy_files(arm_buf, dir_armkbr + "\\exg\\rcv\\1")
                    if not err:
                        if count!=0:
                            self.log_str.emit("Файлы успешно скопированы из буфера в архив {} в кол-ве {}".format(dir_armkbr + "\\exg\\rcv\\1", count), LogType.INFO)
                            # for doc in docs:
                            #     self.log_str.emit(doc, LogType.FILES)

                    self.fe.delete_files(arm_buf)

                self.sleep(2400)
            else:
                self.sleep(600)
