import codecs
from datetime import datetime
import os
import re
from PyQt5.QtCore import QThread
from PyQt5 import QtCore
from libs.LogType import LogType
from libs.FileExplorer import FileExplorer
from contants.path_constants import arm_kbrn_logs, puds_disk, trans_disk

class Viverka(QThread):

    log_str = QtCore.pyqtSignal(str, LogType)

    def __init__(self, button):
        QThread.__init__(self)
        self.fe = FileExplorer()
        self.button = button

    def run(self):
        """Выверка"""
        
        regular = re.compile(r".*_armkbr-n_.*\.log")

        file_names_from_log = []
        current_logs = arm_kbrn_logs + '\\' + datetime.now().strftime("%Y%m%d")
        for file_name in os.listdir(current_logs):
            if regular.search(file_name.lower()) is not None:
                print(file_name)
                # log = open(arm_kbrn_logs + "\\" + file_name,'r')
                # Открываем лог в определнной кодировке
                log = codecs.open(current_logs + "\\" + file_name,'r', 'cp866')
                _files = {}
                for line in log:
                    try:
                        # Сплитаем по определенному символу, чтобы выделить Тип обработчика и само сообщение
                        splitted = line.split('\x04')
                        if splitted.__len__() > 4:
                            type = splitted[4]
                            message = splitted[5]
                            if type == 'kbr-snd':
                                # Просматриваем тип обработчика kbr-snd
                                if message.__contains__('═рўрыю юсЁрсюЄъш Їрщыр'):
                                    # Если сообщение содержит -> Начало обработки файла
                                    spl_message = message.split('═рўрыю юсЁрсюЄъш Їрщыр')
                                    file_name = spl_message[1].replace('\x05\r\n','')
                                    file_name = file_name.replace(' ','')
                                    # Выделяем имя файла и записываем его в словарь со значением False
                                    _files[file_name] = {'sended': False, 'isInArchive': False}
                                
                                if message.__contains__('╘рщы яюьх∙хэ т т√їюфэющ ЁхёєЁё (http://172.16.18.211:7777'):
                                    # Если сообщение содержит -> Файл помещен в выходной ресурс ...
                                    spl_message = message.split(':')
                                    file_name = spl_message[0]
                                    # Обновляем словарь по имени файла(ключу), записываем значение True -> Файл успешно загрузился на ресурс
                                    _files[file_name]['sended'] = True

                    except UnicodeDecodeError as ex:
                        pass
                
                #  Добавляем в конечный массив просмотра файлов, для последующей обработки
                file_names_from_log.append(_files)
                log.close()

        print(file_names_from_log)

        current_date = datetime.now().strftime("%d%m%Y")

        vchera = trans_disk + "\\OUT_OEBS\\4800\\044525000\\" + current_date + "\\1"
        self.fe.check_dir(vchera)

        vcheran = trans_disk + "\\OUT_OEBS\\4800\\004525987\\" + current_date + "\\1"

        self.fe.check_dir(vcheran)

        dir = puds_disk + '\\output\\' + datetime.now().strftime("%Y%m%d") + '\\1'

        self.fe.check_dir(dir)

        dirs = [vchera, vcheran, dir]

        file_names_from_archive = []
        for _dir in dirs:
            files = {}
            for file_name in os.listdir(_dir):
                file_path = _dir + "\\" + file_name
                if os.path.isfile(file_path):
                    files[file_name] = {'isInLog': False, 'sended': False}

            file_names_from_archive.append(files)

        print(file_names_from_archive)

        print('\n')
        for arc_dict in file_names_from_archive:
            for ak, av in arc_dict.items():
                for log_dict in file_names_from_log:
                    try:
                        if ak in log_dict:
                            arc_dict[ak]['isInLog'] = True
                            arc_dict[ak]['sended'] = log_dict[ak]['sended']
                            log_dict[ak]['isInArchive'] = True
                        else:
                            pass
                    except KeyError as ex:
                        print("Ошибка ключа")


        print(file_names_from_log)
        print(file_names_from_archive)
        log_count = 0
        for _dict in  file_names_from_log:
            for k,v in _dict.items():
                if v['sended'] and v['isInArchive']:
                    log_count += 1
                else:
                    message = ''
                    if v['sended'] == False:
                        message += '{} не был отправлен '.format(k)
                    if v['isInArchive'] == False:
                        if message != '':
                            message += ' и не был найден в архивах'
                        else:
                            message += '{} не был найден в архивах'.format(k)

                    self.log_str.emit(message, LogType.INFO)
                    # print(message)
                    
        arc_count = 0
        for _dict in  file_names_from_archive:
            for k,v in _dict.items():
                if v['sended'] and v['isInLog']:
                    arc_count += 1
                else:
                    message = ''
                    if v['sended'] == False:
                        message += '{} не был отправлен '.format(k)
                    if v['isInLog'] == False:
                        if message != '':
                            message += 'и не был найден в логах'
                        else:
                            message += '{} не был найден в логах'.format(k)

                    self.log_str.emit(message, LogType.INFO)
                    # print(message)

        if log_count == arc_count:
            self.log_str.emit("Успешно отправленных файлов {}".format(log_count), LogType.INFO)

        else:
            self.log_str.emit("Расхождение в количестве отправленных документов лог -> {}, архив -> {}".format(log_count, arc_count), LogType.INFO)

        self.button.setDisabled(False)