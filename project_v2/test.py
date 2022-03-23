from asyncio.log import logger
from datetime import datetime
import os
import re
import subprocess
from time import sleep
import codecs

from libs.Logger import Logger
from libs.LogType import LogType
from contants.path_constants import arm_kbrn_logs, trans_disk, puds_disk
from libs.FileExplorer import FileExplorer


# while True:
#     time_now = datetime.time(datetime.now())
#     time_to = datetime.time(datetime.strptime("09:00:00","%H:%M:%S"))
#     time_from = datetime.time(datetime.strptime("20:30:00","%H:%M:%S"))
#     time_between_1 = datetime.time(datetime.strptime("23:59:59","%H:%M:%S"))
#     time_between_2 = datetime.time(datetime.strptime("00:00:00","%H:%M:%S"))
#     if time_now >= time_from and time_now <= time_between_1 or time_now >= time_between_2 and time_now <= time_to:
#         print("True")
#     else: print("False")
    
#     sleep(10)    

fe = FileExplorer()

regular = re.compile(r".*_armkbr-n_.*\.log")

file_names_from_log = []

for file_name in os.listdir(arm_kbrn_logs):
    if regular.search(file_name.lower()) is not None:
        print(file_name)
        # log = open(arm_kbrn_logs + "\\" + file_name,'r')
        # Открываем лог в определнной кодировке
        log = codecs.open(arm_kbrn_logs + "\\" + file_name,'r', 'cp866')
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
fe.check_dir(vchera)

vcheran = trans_disk + "\\OUT_OEBS\\4800\\004525987\\" + current_date + "\\1"

fe.check_dir(vcheran)

dir = puds_disk + '\\output\\' + current_date + '\\1'

fe.check_dir(dir)

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

            print(message)
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

            print(message)

if log_count == arc_count:
    print("Успешно отправленных файлов {}".format(log_count))
else:
    print("Расхождение в количестве отправленных документов лог -> {}, arch -> {}".format(log_count, arc_count))