from datetime import datetime
from PyQt5.QtCore import QThread
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox

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


class EpdDay(QThread):

    log_str = QtCore.pyqtSignal(str, LogType)
    confir_message = QtCore.pyqtSignal(str, str)
    update_counts = QtCore.pyqtSignal(int, int)

    def __init__(self, form):
        QThread.__init__(self)
        self.form = form
        self.fe = FileExplorer()
        self.fe.log_str.connect(form.log)
        self.confirm = None

    def run(self):
        self.form.ui.day.setDisabled(True)
        now_hour = datetime.now().hour
        now_minutes = datetime.time(datetime.now()).__str__()[3]

        if now_hour != 16:
            self.stage1()

        elif now_hour == 16:
            if now_minutes == "4" or now_minutes == "5":
                self.stage1()
            else:
                self.confir_message.emit(
                    "Вопрос",
                    "С 16:00 до 16:30 обычно происходит формирование 'ППБ'. Вы уверены что хотите продолжить загрузку?",
                )

                while self.confirm == None:
                    self.sleep(1)

                if self.confirm == True:
                    self.confirm == None
                    self.stage1()
                else:
                    self.log_str.emit("Выполнение ЭПД день отменено", LogType.INFO)
                    self.confirm = None

        self.form.ui.day.setDisabled(False)

    def stage1(self):

        count = self.fe.count_files_in_folder(
            dir_armkbr + "\\exg\\rcv", filter=r".*ed201.*"
        )[0]

        if count != 0:
            self.stage3(count)
        else:
            self.stage2()

    def stage2(self):

        rcv = dir_armkbr + "\\Exg\\rcv"
        bvp = rcv + "\\211"

        dd = datetime.now().strftime("%d")

        if self.fe.count_files_in_folder(dir_armkbr + "\\exg\\rcv")[0] == 0:
            self.log_str.emit("Нет файлов к отправке!", LogType.INFO)

        else:
            # Проверка ED211 документов
            count_ed211 = 0
            list_of_docs = []
            err, count, docs = self.fe.move_files(
                rcv,
                bvp,
                filter=r".*4525000987000000000000ed2114" + str(dd) + r"01.*\.ed$",
                name_of_doc='ed2114_01'
            )

            if not err:
                count_ed211+=count
                list_of_docs+=docs

            err, count, docs = self.fe.move_files(
                rcv,
                bvp,
                filter=r".*4525000987000000000000ed2114" + str(dd) + r"02.*\.ed$",
                name_of_doc='ed2114_02'
            )

            if not err:
                count_ed211+=count
                list_of_docs+=docs

            err, count, docs = self.fe.move_files(
                rcv,
                bvp,
                filter=r".*4525000987000000000000ed2114" + str(dd) + r"03.*\.ed$",
                name_of_doc='ed2114_03'
            )

            if not err:
                count_ed211+=count
                list_of_docs+=docs

            err, count, docs = self.fe.move_files(
                rcv,
                bvp,
                filter=r".*4525000987000000000000ed2114" + str(dd) + r"04.*\.ed$",
                name_of_doc='ed2114_04'
            )

            if not err:
                count_ed211+=count
                list_of_docs+=docs

            err, count, docs = self.fe.move_files(rcv, bvp, filter=r".*ed211" + str(dd) + r".*\.eds$", name_of_doc='ed211')

            if not err:
                count_ed211+=count
                list_of_docs+=docs
            
            if count_ed211 != 0:
                self.log_str.emit("Документы ED211 успешно перемещены в количестве {} в {}".format(count_ed211, bvp), LogType.INFO)
                for doc in list_of_docs:
                    self.log_str.emit(doc,LogType.FILES)
            else:
                self.log_str.emit("Нет документов ED211 для перемещения.", LogType.INFO)

            self.fe.check_dir(dir_log)
            self.fe.check_dir(dir_armkbr + "\\exg\\rcv")

            current_date = datetime.now().strftime("%d.%m.%Y")

            self.fe.check_dir(dir_archive)
            self.fe.check_dir(arm_buf)

            err, count, docs = self.fe.move_confirms(dir_armkbr + "\\exg\\rcv", dir_armkbr + "\\exg\\rcv\\1") # Исключить квитки без расширения

            if not err:
                self.log_str.emit("Квитки успешно перемещены в архив в количестве {}".format(count), LogType.INFO)
                # for doc in docs:
                #     self.log_str.emit(doc, LogType.FILES)

            err, count, docs = self.fe.move_files(dir_armkbr + "\\exg\\rcv", arm_buf)

            if not err:
                self.log_str.emit("Файлы успешно перемещены в буфер в кол-ве {}".format(count), LogType.INFO)
                # for doc in docs:
                #     self.log_str.emit(doc, LogType.FILES)

            self.fe.decode_files(unb64_rabis, arm_buf, dir_log)

            arc_dir = dir_archive + "\\" + current_date + "\\uarm3\\inc\\ed"

            self.fe.check_dir(arc_dir)
            
            arc_xml_count = 0
            doc_xml_list = []
            err, count, docs = self.fe.copy_files(arm_buf, arc_dir, r".*\.ed\.xml$", name_of_doc='xml')
            if not err:
                arc_xml_count+=count
                doc_xml_list+=docs

            err, count, docs = self.fe.copy_files(arm_buf, arc_dir, r".*ed211.*\.ed\.xml$", name_of_doc='e211.ed.xml')
            if not err:
                arc_xml_count+=count
                doc_xml_list+=docs

            if arc_xml_count != 0:
                self.log_str.emit("xml успешно скопированы в архив в кол-ве {} в {}".format(arc_xml_count, arc_dir), LogType.INFO)
                # for doc in doc_xml_list:
                #     self.log_str.emit(doc, LogType.FILES)
            else:
                self.log_str.emit("Нет документов xml для перемещения в архив.", LogType.INFO)

            trans_disk_path = trans_disk + "IN_OEBS_BIK\\044525000"

            rash = "D:\\rash\\ED808"

            self.fe.check_dir(rash)

            xml_to_trans_disk_count = 0
            xml_to_trans_docs_list = []
            err, count,docs = self.fe.copy_files(arm_buf, trans_disk_path, r".*\.ed\.xml$", name_of_doc='ed.xml', default_check=False)
            if not err:
                xml_to_trans_disk_count+=count
                xml_to_trans_docs_list+=docs
            err, count, docs = self.fe.copy_files(arm_buf, trans_disk_path, r".*ed211.*\.ed\.xml$", name_of_doc='ed211.xml', default_check=False)
            if not err:
                xml_to_trans_disk_count+=count
                xml_to_trans_docs_list+=docs

            if xml_to_trans_disk_count != 0:
                self.log_str.emit("xml успешно скопированы на транспортный диск в кол-ве {}".format(xml_to_trans_disk_count), LogType.INFO)
                for doc in xml_to_trans_docs_list:
                    self.log_str.emit(doc, LogType.FILES)

                self.update_counts.emit(0, xml_to_trans_disk_count)

            else:
                self.log_str.emit("Нет документов xml для перемещения в архив.", LogType.INFO)



            err, count,docs = self.fe.copy_files(arm_buf, rash, r".*ed808.*\.eds\.xml$", name_of_doc='ed808.xml')
            if not err:
                if count!=0:
                    self.log_str.emit("ed808 успешно скопированы в кол-ве {} в {}".format(count, rash), LogType.INFO)
                    for doc in docs:
                        self.log_str.emit(doc, LogType.FILES)
                    
                else:
                     self.log_str.emit("ed808 отсутствуют", LogType.INFO)


            ed_count = 0
            ed_docs_list = []
            err, count, docs = self.fe.copy_files(arm_buf, puds_disk + "input", r".*\.ed$", name_of_doc='.eds', default_check=False)
            if not err:
                ed_count+=count
                ed_docs_list+=docs
            err, count, docs = self.fe.copy_files(arm_buf, puds_disk + "input", r".*ed211.*\.eds$", name_of_doc='ed211.eds', default_check=False)
            if not err:
                ed_count+=count
                ed_docs_list+=docs

            if ed_count!=0:
                self.log_str.emit("ed и eds успешно скопированы в кол-ве {} на диск ПУДС".format(ed_count),LogType.INFO)
                for doc in ed_docs_list:
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

    def stage3(self, count_ed201):
        self.confir_message.emit(
            "Вопрос",
            "Среди документов для загрузки найдено {} - ED201. Вы уверены что хотите продолжить загрузку?".format(
                count_ed201
            ),
        )

        while self.confirm == None:
            self.sleep(1)

        if self.confirm == True:
            self.confirm == None
            self.stage2()
        else:
            self.log_str.emit("Выполнение ЭПД день отменено", LogType.INFO)
            self.confirm = None
