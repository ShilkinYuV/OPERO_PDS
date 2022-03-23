import os
import re
import shutil
from xml.dom import minidom
from PyQt5 import QtWidgets, QtCore, QtGui
from libs.LogType import LogType

class FileExplorer(QtCore.QObject):
    log_str = QtCore.pyqtSignal(str, LogType)

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
        confirm_count = 0
        for file_name in os.listdir(path=path):
            if os.path.isfile(path + "\\" + file_name):
                if filter is not None:
                    if regular.search(file_name.lower()) is not None:
                        if file_name.__contains__('.') == True:
                            count += 1
                        else:
                            confirm_count += 1
                else:
                    if file_name.__contains__('.') == True:
                        count += 1
                    else:
                        confirm_count += 1

        return [count, confirm_count]

    def move_confirms(self, path_from, path_to):
        self.check_dir(path_to)
        message = "Непредвиденная ошибка при перемещении квитков в " + path_to

        listdir = []
        # Перемещение файлов
        for file_name in os.listdir(path=path_from):
            if os.path.isfile(path_from + "\\" + file_name):
                if file_name.__contains__('.') == False:
                    try:
                        if os.path.exists(path_to + "\\" + file_name) == False:
                            listdir.append(file_name)
                            shutil.move(path_from + "\\" + file_name, path_to)
                        else:
                            self.log("Файл {} уже пристутсвует в {}".format(file_name, path_to), log_type=LogType.WARNING)
                    except Exception as ex:
                        self.log(message + ' file_name= {}\\{}'.format(path_from,
                                 file_name), log_type=LogType.ERROR)

        # Проверка, переместились ли файлы
        count,file_name_failed = self.check_move_or_copy_files(listdir, path_from, path_to)
        if count == 0:
            self.log(
                "Все файлы [Квитки] в количестве {} успешно перемещены из [{}] в [{}]".format(
                    len(listdir), path_from, path_to
                ), log_type=LogType.DEBUG
            )
        
            return False, len(listdir), listdir

        elif count is None:
            self.log(
                "Нет файлов [Квитки] для перемещения из [{}] в [{}]".format(
                    path_from, path_to
                ), log_type=LogType.DEBUG
            )

            return False, 0, []

        else:
            self.log(
                "Не удалось переместить {} файлов [Квитки] из [{}] в [{}]".format(
                    count, path_from, path_to
                ), log_type=LogType.ERROR
            )

            return True, count, file_name_failed

    def move_files(self, path_from, path_to, filter=None, name_of_doc='все', default_check=True):
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
                            if os.path.exists(path_to + "\\" + file_name) == False:
                                listdir.append(file_name)
                                shutil.move(path_from + "\\" + file_name, path_to)
                            else:
                                self.log("Файл {} уже пристутсвует в {}".format(file_name, path_to), log_type=LogType.WARNING)
                        except Exception as ex:
                            self.log(
                                message + ' file_name= {}\\{}'.format(path_from, file_name), log_type=LogType.ERROR)
                else:
                    try:
                        if os.path.exists(path_to + "\\" + file_name) == False:
                            listdir.append(file_name)
                            shutil.move(path_from + "\\" + file_name, path_to)
                        else:
                            self.log("Файл {} уже пристутсвует в {}".format(file_name, path_to), log_type=LogType.WARNING)
                    except Exception as ex:
                        self.log(message + ' file_name= {}\\{}'.format(path_from,
                                 file_name), log_type=LogType.ERROR)

        # Проверка, переместились ли файлы
        
        count,file_name_failed = self.check_move_or_copy_files(listdir, path_from, path_to)
        if count == 0:
            self.log(
                "Все файлы [{}] в количестве {} успешно перемещены из [{}] в [{}]".format(
                    name_of_doc, len(listdir), path_from, path_to
                ), log_type=LogType.DEBUG
            )
            return False, len(listdir), listdir

        elif count is None:
            self.log(
                "Нет файлов [{}] для перемещения из [{}] в [{}]".format(
                    name_of_doc, path_from, path_to
                ), log_type=LogType.DEBUG
            )

            return False, 0, []

        else:
            self.log(
                "Не удалось переместить {} файлов [{}] из [{}] в [{}]".format(
                    count, name_of_doc, path_from, path_to
                ), log_type=LogType.ERROR
            )
            return True, count, file_name_failed

    def copy_files(self, path_from, path_to, filter=None, name_of_doc='все', default_check=True):
        """Копирование файлов из одной директории в другую.
        Используя регулярное (filter) выражение, можно скопировать определенные файлы"""
        self.check_dir(path_to)

        if filter is not None:
            regular = re.compile(filter)

        listdir = []
        file_name_failed = []
        count = 0
        count_before = 0
        alr_exists_count = 0
        # Копирование файлов
        for file_name in os.listdir(path=path_from):
            file_path = path_from + "\\" + file_name
            message = "Непредвиденная ошибка при копировании файла в " + path_to
            if os.path.isfile(file_path):
                if filter is not None:
                    if regular.search(file_name.lower()) is not None:
                        count_before += 1
                        try:
                            if os.path.exists(path_to + "\\" + file_name) == False:
                                shutil.copy2(file_path, path_to)
                                listdir.append(file_name)
                                count+=1
                            elif name_of_doc == 'log':
                                shutil.copy2(file_path, path_to)
                                listdir.append(file_name)
                            else:
                                self.log("Файл {} уже пристутсвует в {}".format(file_name, path_to), log_type=LogType.WARNING)
                                alr_exists_count+=1
                                file_name_failed.append(file_name)

                        except Exception as ex:
                            self.log(
                                message + ' file_name= {}\\{}'.format(path_from, file_name), log_type=LogType.ERROR)
                            file_name_failed.append(file_name)
                else:
                    count_before += 1
                    try:
                        if os.path.exists(path_to + "\\" + file_name) == False:
                            shutil.copy2(file_path, path_to)
                            listdir.append(file_name)
                            count+=1
                        else:
                                self.log("Файл {} уже пристутсвует в {}".format(file_name, path_to), log_type=LogType.WARNING)
                                file_name_failed.append(file_name)
                                alr_exists_count+=1
                    except:
                        self.log(message + ' file_name= {}\\{}'.format(path_from,
                                 file_name), log_type=LogType.ERROR)
                        file_name_failed.append(file_name)

        # Проверка, скопировались ли файлы
        if count == count_before:
            self.log(
                "Все файлы [{}] в количестве {} успешно скопированы из [{}] в [{}]".format(
                    name_of_doc, len(listdir), path_from, path_to
                ), log_type=LogType.DEBUG
            )

            return False, len(listdir), listdir

        elif count is None:
            self.log(
                "Нет файлов [{}] для копирования из [{}] в [{}]".format(
                    name_of_doc, path_from, path_to
                ), log_type=LogType.DEBUG
            )
        
            return False, 0, []

        elif count != count_before and count_before-count==alr_exists_count:
            self.log(
                "Из [{}] {} файлов [{}] переместились {}, {} уже присутствует в {} ".format(
                    path_from ,count_before, name_of_doc, count, alr_exists_count, path_to
                ), log_type=LogType.WARNING
            )

            return False, count, listdir

    def delete_files(self, path_from, filter=None, name_of_doc=''):
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
                            self.log(message, log_type=LogType.ERROR)
                else:
                    try:
                        os.remove(file_path)
                        listdir.append(file_name)
                    except Exception as ex:
                        self.log(message, log_type=LogType.ERROR)

        # Проверка, удалились ли файлы

        delete_list_dir = os.listdir(path=path_from)
        not_deleted_files = []
        count = 0
        for file_name in listdir:
            try:
                delete_list_dir.index(file_name)
                count += 1
                not_deleted_files.append(file_name)
            except ValueError as ex:
                pass

        if count == 0:
            self.log("Все файлы успешно удалены", log_type=LogType.DEBUG)
            return False,0, []

        else:
            self.log(
                "Не удалось удалить {count} файлов".format(count=count), log_type=LogType.ERROR
            )
            return True,len(not_deleted_files),not_deleted_files

    def decode_files(self, decoder, arm_buf, dir_log):
        """Расшифровка файлов по указанному пути, с проверкой"""
        count_before = self.count_files_in_folder(arm_buf)[0]
        files_before = []
        for file_name in os.listdir(arm_buf):
            if os.path.isfile(arm_buf + '\\' + file_name):
                files_before.append(file_name)

        os.system(
            "{decoder} *.* {buffer}\ {buffer}\ >> {logs}\decod.log".format(
                decoder=decoder, buffer=arm_buf, logs=dir_log
            )
        )

        count_after = self.count_files_in_folder(arm_buf)[0]
        decode_files = []
        for file_name in os.listdir(arm_buf):
            if os.path.isfile(arm_buf + '\\' + file_name):
                flag = False
                for file in files_before:
                    if file == file_name:
                        flag = True
                
                if flag is False:
                    decode_files.append(file_name)


        if count_before == 0:
            self.log("Нет файлов для расшифровки", LogType.INFO)
        elif count_before == count_after - count_before:
            self.log("Все файлы успешно расшифрованы - {}".format(count_before), log_type=LogType.INFO)
            for file in decode_files:
                self.log(file, log_type=LogType.DEBUG)
        else:
            undecode_count = count_before - (count_after - count_before)
            self.log(
                "Ошибка расшифровки! Из {} не расшифровано {}.".format(
                    count_before, undecode_count
                ), log_type=LogType.ERROR
            )

    def check_move_or_copy_files(self, listdir_from, path_from, path_to):
        """Проверка переместились ли файлы в нужную дерикторию"""
        count = 0
        file_name_failed = []
        if len(listdir_from) != 0:
            move_to_listdir = os.listdir(path=path_to)
            for file_name in listdir_from:
                try:
                    move_to_listdir.index(file_name)
                except ValueError as ex:
                    count += 1
                    file_name_failed.append(file_name)

            if count == 0:
                return 0, []

            elif count > 0:
                return count, file_name_failed

        return 0, []

    def log(self, message, log_type):
        self.log_str.emit(message, log_type)
        print(message)

