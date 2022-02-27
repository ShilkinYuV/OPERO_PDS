import os
import re
import shutil


class FileExplorer:
    def __init__(self, _logger=None):
        if _logger is not None:
            self.logger = _logger

    def check_dir(self, path):
        """Проверка наличия директории и создание ее в случае отсутствия"""
        if not os.path.exists(path=path):
            os.makedirs(path)

    def count_files_in_folder(self, path):
        """Вывод количества файлов по указанному пути"""
        count = 0
        for file_name in os.listdir(path=path):
            if os.path.isfile(path + "\\" + file_name):
                count += 1

        return count

    def move_files(self, path_from, path_to):
        """Перемещение файлов из одного пути в другой, с проверкой наличия в новой директории"""
        self.check_dir(path_to)

        listdir = []
        # Перемещение файлов
        for file_name in os.listdir(path=path_from):
            if os.path.isfile(path_from + "\\" + file_name):
                try:
                    listdir.append(file_name)
                    shutil.move(path_from + "\\" + file_name, path_to)
                except Exception as ex:
                    message = (
                        "Непредвиденная ошибка при перемещении файлов в " + path_to
                    )
                    self.log(message, True)

        # Проверка, переместились ли файлы
        self.check_move_or_copy_files(listdir, path_to)


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
        self.check_move_or_copy_files(listdir, path_to)
        

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
                message = "Непредвиденная ошибка при удалении файла {file}".format(file=file_name)
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
                count+=1
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
            self.log("Ошибка расшифровки! Из {} расшифровано {}.".format(count_before,undecode_count))



    def check_move_or_copy_files(self, listdir_from, path_to):
        """Проверка переместились ли файлы в нужную дерикторию"""
        move_to_listdir = os.listdir(path=path_to)
        count = 0
        for file_name in listdir_from:
            try:
                move_to_listdir.index(file_name)
            except ValueError as ex:
                count += 1
                # self.logger.log("{file_name} не переместился в " + path_to,isError=True)

        if count == 0:
            self.log("Все файлы успешно перемещены/скопированы {}".format(len(listdir_from)))

        else:
            self.log(
                "Не удалось переместить/скопировать {count} файлов".format(count=count),
                isError=True,
            )

    def log(self, message, isError=False):
        if self.logger is not None:
            self.logger.log(message, isError=isError)
        else:
            print(message)