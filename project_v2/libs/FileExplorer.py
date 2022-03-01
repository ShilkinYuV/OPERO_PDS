import os
import re
import shutil
from xml.dom import minidom
from PyQt5 import QtWidgets, QtCore, QtGui


class FileExplorer(QtCore.QObject):
    log_str = QtCore.pyqtSignal(str, bool, bool)

    def __init__(self):
        super(FileExplorer, self).__init__()

    def check_dir(self, path):
        """Проверка наличия директории и создание ее в случае отсутствия"""
        if not os.path.exists(path=path):
            os.makedirs(path)

    def count_files_in_folder(self, path, filter=None):
        """Вывод количества файлов по указанному пути"""

        if filter is not None:
            regular = re.compile(filter)

        count = 0
        for file_name in os.listdir(path=path):
            if os.path.isfile(path + "\\" + file_name):
                if filter is not None:
                    if regular.search(file_name.lower()) is not None:
                        count += 1
                else:
                    count += 1

        return count

    def move_files(self, path_from, path_to, filter=None):
        """Перемещение файлов из одного пути в другой, с проверкой наличия в новой директории"""
        self.check_dir(path_to)

        if filter is not None:
            regular = re.compile(filter)
            print(filter)

        message = "Непредвиденная ошибка при перемещении файлов в " + path_to

        listdir = []
        # Перемещение файлов
        for file_name in os.listdir(path=path_from):
            if os.path.isfile(path_from + "\\" + file_name):
                if filter is not None:
                    if regular.search(file_name.lower()) is not None:
                        try:
                            listdir.append(file_name)
                            shutil.move(path_from + "\\" + file_name, path_to)
                        except Exception as ex:
                            self.log(message, True)
                else:
                    try:
                        listdir.append(file_name)
                        shutil.move(path_from + "\\" + file_name, path_to)
                    except Exception as ex:
                        self.log(message, True)

        # Проверка, переместились ли файлы
        count = self.check_move_or_copy_files(listdir, path_from, path_to)
        if count == 0:
            self.log(
                "Все файлы успешно в количестве {} перемещены из [{}] в [{}]".format(
                    len(listdir), path_from, path_to
                )
            )

        else:
            self.log(
                "Не удалось переместить {} файлов из {} в {}".format(
                    count, path_from, path_to
                ),
                isError=True,
            )

    def copy_files(self, path_from, path_to, filter=None):
        """Копирование файлов из одной директории в другую.
        Используя регулярное (filter) выражение, можно скопировать определенные файлы"""
        self.check_dir(path_to)

        if filter is not None:
            regular = re.compile(filter)

        listdir = []
        # Копирование файлов
        for file_name in os.listdir(path=path_from):
            file_path = path_from + "\\" + file_name
            message = "Непредвиденная ошибка при копировании файла в " + path_to
            if os.path.isfile(file_path):
                if filter is not None:
                    if regular.search(file_name.lower()) is not None:
                        try:
                            shutil.copy2(file_path, path_to)
                            listdir.append(file_name)
                        except Exception as ex:
                            self.log(message, True)
                else:
                    try:
                        shutil.copy2(file_path, path_to)
                        listdir.append(file_name)
                    except:
                        self.log(message, True)

        # Проверка, скопировались ли файлы
        count = self.check_move_or_copy_files(listdir, path_from, path_to)
        if count == 0:
            self.log(
                "Все файлы успешно в количестве {} скопированы из [{}] в [{}]".format(
                    len(listdir), path_from, path_to
                )
            )

        else:
            self.log(
                "Не удалось скопировать {} файлов из {} в {}".format(
                    count, path_from, path_to
                ),
                isError=True,
            )

    def delete_files(self, path_from, filter=None):
        """Удаление файлов из директории.
        Используя регулярное (filter) выражение, можно удалить определенные файлы"""

        listdir = []

        if filter is not None:
            regular = re.compile(filter)

        # Удаление файлов
        for file_name in os.listdir(path=path_from):
            file_path = path_from + "\\" + file_name
            if os.path.isfile(file_path):
                message = "Непредвиденная ошибка при удалении файла {file}".format(
                    file=file_name
                )
                if filter is not None:
                    if regular.search(file_name.lower()) is not None:
                        try:
                            os.remove(file_path)
                            listdir.append(file_name)
                        except Exception as ex:
                            self.log(message, isError=True)
                else:
                    try:
                        os.remove(file_path)
                        listdir.append(file_name)
                    except Exception as ex:
                        self.log(message, isError=True)

        # Проверка, удалились ли файлы

        delete_list_dir = os.listdir(path=path_from)
        count = 0
        for file_name in listdir:
            try:
                delete_list_dir.index(file_name)
                count += 1
            except ValueError as ex:
                pass

        if count == 0:
            self.log("Все файлы успешно удалены")

        else:
            self.log(
                "Не удалось удалить {count} файлов".format(count=count),
                isError=True,
            )

    def decode_files(self, decoder, arm_buf, dir_log):
        """Расшифровка файлов по указанному пути, с проверкой"""
        count_before = self.count_files_in_folder(arm_buf)

        os.system(
            "{decoder} *.* {buffer}\ {buffer}\ >> {logs}\decod.log".format(
                decoder=decoder, buffer=arm_buf, logs=dir_log
            )
        )

        count_after = self.count_files_in_folder(arm_buf)

        if count_before == count_after - count_before:
            self.log("Все файлы успешно расшифрованы - {}".format(count_before))

        else:
            undecode_count = count_before - (count_after - count_before)
            self.log(
                "Ошибка расшифровки! Из {} не расшифровано {}.".format(
                    count_before, undecode_count
                ),
                isError=True,
            )

    def check_move_or_copy_files(self, listdir_from, path_from, path_to):
        """Проверка переместились ли файлы в нужную дерикторию"""
        count = 0
        if len(listdir_from) != 0:
            move_to_listdir = os.listdir(path=path_to)
            for file_name in listdir_from:
                try:
                    move_to_listdir.index(file_name)
                except ValueError as ex:
                    count += 1

            if count == 0:
                return count

            else:
                return count

    def log(self, message, isError=False):
        if self.logger is not None:
            self.log_str.emit(message, False, isError)
        else:
            print(message)

    def check_dir_for_docs(self, rnp, path_from, path_to):
        archive = path_from + "\\1"
        self.check_dir(archive)
        self.check_dir(path_to)

        count = 0
        for file_name in os.listdir(path_from):
            file_path = path_from + "\\" + file_name
            if os.path.isfile(file_path):
                mydoc = minidom.parse(file_path)
                items = mydoc.getElementsByTagName("sen:Object")
                for elem in items:
                    self.elementXML = str(elem.firstChild.data)
                    if self.elementXML.__contains__(rnp):
                        self.copy_files(path_from, path_to, filter=file_name.lower())
                        self.move_files(path_from, archive, filter=file_name.lower())
                        count += 1

        return count

    def check_dirs_for_send_docs(self, rnp_folders, rnp_doc_types, dir_armkbrn):
        """Проверка наличия документов на отправку"""

        isEmpty = True
        print(rnp_doc_types)
        for k, v in rnp_doc_types.items():
            count = 0
            for folder in rnp_folders:
                self.check_dir(folder)
                for file_name in os.listdir(folder):
                    file_path = folder + "\\" + file_name
                    if os.path.isfile(file_path):
                        mydoc = minidom.parse(file_path)
                        items = mydoc.getElementsByTagName("sen:Object")
                        for elem in items:
                            self.elementXML = str(elem.firstChild.data)
                            if self.elementXML.__contains__(v):
                                isEmpty = False
                                count += 1
            if count != 0:
                self.log(
                    "Найдены документы типа - {}, в количестве {}".format(k, count)
                )

        count = self.count_files_in_folder(dir_armkbrn)
        if count != 0:
            isEmpty = False
            self.log("Найдены документы для отправки ЭПД в количестве {}".format(count))

        if isEmpty:
            self.log("Документов для отправки не найдено")
