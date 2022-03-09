from datetime import datetime
from PyQt5.QtCore import QThread
from PyQt5 import QtCore
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


class NightCicle(QThread):

    log_str = QtCore.pyqtSignal(str, LogType)
    update_counts = QtCore.pyqtSignal(int, int)

    def __init__(self,form):
        QThread.__init__(self)
        self.work = True
        self.file_explorer = FileExplorer()
        self.file_explorer.log_str.connect(form.log)

    def run(self):
        while self.work:
            time_now = datetime.time(datetime.now())
            time_to = datetime.time(datetime.strptime("09:00:00","%H:%M:%S"))
            time_from = datetime.time(datetime.strptime("20:30:00","%H:%M:%S"))
            # C 20:30 до 9 00 
            if time_to < time_now and time_now > time_from:
                self.file_explorer.check_dir(dir_log)
                self.file_explorer.check_dir(dir_armkbr + "\\exg\\rcv")

                current_date = datetime.now().strftime("%d.%m.%Y")

                if self.file_explorer.count_files_in_folder(dir_armkbr + "\\exg\\rcv") == 0:
                    self.log_str.emit("Нет файлов к отправке!", LogType.INFO)

                else:
                    self.file_explorer.check_dir(dir_archive)
                    self.file_explorer.check_dir(arm_buf)

                    err, count, docs = self.file_explorer.move_confirms(dir_armkbr + "\\exg\\rcv", dir_armkbr + "\\exg\\rcv\\1") # Исключить квитки без расширения
                    if not err:
                        self.log_str.emit("Квитки успешно перемещены в архив в количестве {}".format(count), LogType.INFO)
                        # for doc in docs:
                        #     self.log_str.emit(doc, LogType.FILES)

                    err, count, docs = self.file_explorer.move_files(dir_armkbr + "\\exg\\rcv", arm_buf)
                    if not err:
                        self.log_str.emit("Файлы успешно перемещены в буфер в кол-ве {}".format(count), LogType.INFO)
                        # for doc in docs:
                        #     self.log_str.emit(doc, LogType.FILES)


                    self.file_explorer.decode_files(unb64_rabis, arm_buf, dir_log)

                    arc_dir = dir_archive + "\\" + current_date + "\\uarm3\\inc\\ed"

                    self.file_explorer.check_dir(arc_dir)


                    arc_xml_count = 0
                    arc_doc_list = []
                    err, count, docs = self.fe.copy_files(arm_buf, arc_dir, r".*\.ed\.xml$", name_of_doc='xml')
                    if not err:
                        arc_xml_count+=count
                        arc_doc_list+=docs

                    err, count, docs = self.fe.copy_files(arm_buf, arc_dir, r".*ed211.*\.ed\.xml$", name_of_doc='xml')
                    if not err:
                        arc_xml_count+=count
                        arc_doc_list+=doc

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
                    err, count, docs = self.fe.copy_files(arm_buf, trans_disk_path, r".*ed211.*\.ed\.xml$", name_of_doc='ed211.ed.xml', default_check=False)
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


                    self.file_explorer.delete_files(arm_buf, r".*\.xml$", name_of_doc='.xml')

                    err, count, docs = self.fe.copy_files(arm_buf, dir_armkbr + "\\exg\\rcv\\1")
                    if not err:
                        if count!=0:
                            self.log_str.emit("Файлы успешно скопированы из буфера в архив {} в кол-ве {}".format(dir_armkbr + "\\exg\\rcv\\1", count), LogType.INFO)
                            # for doc in docs:
                            #     self.log_str.emit(doc, LogType.FILES)

                    self.file_explorer.delete_files(arm_buf)

                self.sleep(3600)
            else:
                self.sleep(3600)
