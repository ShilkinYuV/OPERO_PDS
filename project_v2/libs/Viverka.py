import codecs
from datetime import datetime
from distutils.log import Log
import os
import re
from PyQt5.QtCore import QThread
from PyQt5 import QtCore
from libs.LogType import LogType
from libs.FileExplorer import FileExplorer
from contants.path_constants import arm_kbrn_logs, puds_disk, trans_disk, dir_armkbr, dir_archive

class Viverka(QThread):

    log_str = QtCore.pyqtSignal(str, LogType)

    def __init__(self, button):
        QThread.__init__(self)
        self.fe = FileExplorer()
        self.button = button

    def run(self):
        """Выверка"""
        self.log_str.emit("", LogType.SPACE)
        self.log_str.emit("Старт сверки отправленных документов", LogType.INFO)
        
        self.run_cli()

        self.log_str.emit("", LogType.SPACE)
        self.log_str.emit("Старт сверки загруженных документов", LogType.INFO)
        

        self.run_rcv()
        
        self.button.setDisabled(False)

    def run_cli(self):
        warning_count = 0
        regular = re.compile(r".*_armkbr-n_.*\.log")

        file_names_from_log = []
        current_logs = arm_kbrn_logs + '\\' + datetime.now().strftime("%Y%m%d")
        self.fe.check_dir(current_logs)
        for file_name in os.listdir(current_logs):
            if regular.search(file_name.lower()) is not None:
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

                    warning_count += 1
                    self.log_str.emit(message, LogType.WARNING)
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

                    warning_count +=1
                    self.log_str.emit(message, LogType.WARNING)
                    # print(message)

        if log_count == arc_count:
            self.log_str.emit("Успешно отправленных файлов {}".format(log_count), LogType.INFO)

        else:
            self.log_str.emit("Расхождение в количестве отправленных документов лог -> {}, архив -> {}".format(log_count, arc_count), LogType.INFO)

        if warning_count != 0:
            self.log_str.emit("Проблемных файлов {}".format(warning_count), LogType.WARNING)
            

    def run_rcv(self):
        warning_count = 0
        regular = re.compile(r".*_armkbr-n_.*\.log")

        file_names_from_log = []
        _log_dir = arm_kbrn_logs + '\\' + datetime.now().strftime("%Y%m%d")
        self.fe.check_dir(_log_dir)
        for file_name in os.listdir(_log_dir):
            if regular.search(file_name.lower()) is not None:
                log = codecs.open(_log_dir + "\\" + file_name,'r', 'cp866')
                _files = {}
                for line in log:
                    try:
                        # Сплитаем по определенному символу, чтобы выделить Тип обработчика и само сообщение
                        splitted = line.split('\x04')
                        if splitted.__len__() > 4:
                            type = splitted[4]
                            message = splitted[5]
                            if type == 'kbr-rcv':
                                # Просматриваем тип обработчика kbr-snd
                                if message.__contains__('═рўрыю юсЁрсюЄъш Їрщыр'):
                                    # Если сообщение содержит -> Начало обработки файла
                                    spl_message = message.split('═рўрыю юсЁрсюЄъш Їрщыр')
                                    file_name = spl_message[1].replace('\x05\r\n','')
                                    file_name = file_name.replace(' ','')
                                    # Выделяем имя файла и записываем его в словарь со значением False
                                    if file_name.__contains__('.') == True:
                                        _files[file_name] = {'loaded': False, 'isInArchive': False}
                                
                                if message.__contains__('╘рщы яюьх∙хэ т т√їюфэющ ЁхёєЁё (file://C:\oev\exg\\rcv)'):
                                    # Если сообщение содержит -> Файл помещен в выходной ресурс ...
                                    spl_message = message.split(':')
                                    file_name = spl_message[0]
                                    # Обновляем словарь по имени файла(ключу), записываем значение True -> Файл успешно загрузился на ресурс
                                    try:
                                        if file_name.__contains__('.') == True:
                                            _files[file_name]['loaded'] = True
                                    except KeyError:
                                        print("Нет такого файла в списке")

                    except UnicodeDecodeError as ex:
                        pass
                
                #  Добавляем в конечный массив просмотра файлов, для последующей обработки
                file_names_from_log.append(_files)
                log.close()

        """ Получаем имена фалов с архива """

        current_date = datetime.now().strftime("%d%m%Y")

        rcv = dir_armkbr + "\\Exg\\rcv\\1"
        bvp = rcv + "\\211"
        arc_dir = dir_archive + "\\" + datetime.now().strftime("%d.%m.%Y") + "\\uarm3\\inc\\ed"

        self.fe.check_dir(rcv)
        self.fe.check_dir(bvp)
        self.fe.check_dir(arc_dir)

        # fe.check_dir()

        arc_dirs = [rcv, bvp]
        xml_dir = [arc_dir,]

        file_names_from_archive = []
        file_names_from_archive_xml = []


        for _dir in arc_dirs:
            files = {}
            for file_name in os.listdir(_dir):
                file_path = _dir + "\\" + file_name
                if os.path.isfile(file_path) and file_name.__contains__('.') == True:
                    files[file_name] = {'isInLog': False, 'loaded': False, 'decode_vers': False}

            file_names_from_archive.append(files)

        for _dir in xml_dir:
            files = {}
            for file_name in os.listdir(_dir):
                file_path = _dir + "\\" + file_name
                if os.path.isfile(file_path) and file_name.__contains__('.') == True:
                    files[file_name] = {'loaded': False, 'not_decode_vers': False}

            file_names_from_archive_xml.append(files)

        """ Производим сверку """

        for xml_dict in file_names_from_archive_xml:
            for xml_k, xml_v in xml_dict.items():
                for arc_dict in file_names_from_archive:
                    for ak, av in arc_dict.items():
                        try:
                            if xml_k[:-4].lower() == ak.lower():
                                arc_dict[ak]['decode_vers'] = True
                                xml_dict[xml_k]['not_decode_vers'] = True
                        except KeyError as ex:
                            print('Ошибка ключа')

        xml_count = 0
        for xml_dict in file_names_from_archive_xml:
            for xml_k, xml_v in xml_dict.items():
                if xml_v['not_decode_vers'] == False:
                    self.log_str.emit('Нет нерасширофанной версии файла {}'.format(xml_k), LogType.WARNING)
                    xml_count += 1
        count = 0
        for arc_dict in file_names_from_archive:
            for ak, av in arc_dict.items():
                if av['decode_vers'] == False:
                    self.log_str.emit('Нет расширофанной версии файла {}'.format(ak), LogType.WARNING)
                    count += 1

        if count == 0 and xml_count == 0:
            self.log_str.emit('Архивы расшифрованных и нерасшифрованных совпадают.', LogType.INFO)



        for arc_dict in file_names_from_archive:
            for ak, av in arc_dict.items():
                for log_dict in file_names_from_log:
                    try:
                        if ak in log_dict:
                            arc_dict[ak]['isInLog'] = True
                            arc_dict[ak]['loaded'] = log_dict[ak]['loaded']
                            log_dict[ak]['isInArchive'] = True

                    except KeyError as ex:
                        print("Ошибка ключа")

        log_count = 0
        for _dict in  file_names_from_log:
            for k,v in _dict.items():
                if v['loaded'] and v['isInArchive']:
                    log_count += 1
                else:
                    message = ''
                    if v['loaded'] == False:
                        message += '{} не был отправлен '.format(k)
                    if v['isInArchive'] == False:
                        if message != '':
                            message += ' и не был найден в архивах'
                        else:
                            message += '{} не был найден в архивах'.format(k)
                    warning_count += 1
                    self.log_str.emit(message, LogType.WARNING)

        arc_count = 0
        for _dict in  file_names_from_archive:
            for k,v in _dict.items():
                if v['loaded'] and v['isInLog']:
                    arc_count += 1
                else:
                    message = ''
                    if v['loaded'] == False:
                        message += '{} не был отправлен '.format(k)
                    if v['isInLog'] == False:
                        if message != '':
                            message += 'и не был найден в логах'
                        else:
                            message += '{} не был найден в логах'.format(k)
                    warning_count += 1
                    self.log_str.emit(message, LogType.WARNING)

        if log_count == arc_count:
            self.log_str.emit("Успешно отправленных файлов {}".format(log_count), LogType.INFO)
        else:
            self.log_str.emit("Расхождение в количестве отправленных документов лог -> {}, arch -> {}".format(log_count, arc_count), LogType.WARNING)
        if warning_count != 0:
            self.log_str.emit("Проблемных файлов {}".format(warning_count), LogType.WARNING)

        