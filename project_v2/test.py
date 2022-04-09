from asyncio.log import logger
from datetime import datetime, timedelta
import os
import re
import subprocess
from time import sleep
import codecs

from libs.Logger import Logger
from libs.LogType import LogType
from contants.path_constants import arm_kbrn_logs, dir_armkbr, dir_archive
from libs.FileExplorer import FileExplorer

date = datetime.strptime("09:00:00 10.01.2022","%H:%M:%S %d.%m.%Y")

d = date - timedelta(days=1)
if d.day.__str__().__len__() == 1:
    print("0{}".format(d.day.__str__()))
else:
    print(d.day)

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

# fe = FileExplorer()

""" Получаем имена фалов из логов """

# regular = re.compile(r".*_armkbr-n_.*\.log")

# file_names_from_log = []
# _log_dir = arm_kbrn_logs + '\\' + datetime.now().strftime("%Y%m%d")
# fe.check_dir(_log_dir)
# for file_name in os.listdir(_log_dir):
#     if regular.search(file_name.lower()) is not None:
#         print(file_name)
#         # log = open(arm_kbrn_logs + "\\" + file_name,'r')
#         # Открываем лог в определнной кодировке
#         log = codecs.open(_log_dir + "\\" + file_name,'r', 'cp866')
#         _files = {}
#         for line in log:
#             try:
#                 # Сплитаем по определенному символу, чтобы выделить Тип обработчика и само сообщение
#                 splitted = line.split('\x04')
#                 if splitted.__len__() > 4:
#                     print(type)
#                     type = splitted[4]
#                     message = splitted[5]
#                     if type == 'kbr-rcv':
#                         print(message)
#                         # Просматриваем тип обработчика kbr-snd
#                         if message.__contains__('═рўрыю юсЁрсюЄъш Їрщыр'):
#                             # Если сообщение содержит -> Начало обработки файла
#                             spl_message = message.split('═рўрыю юсЁрсюЄъш Їрщыр')
#                             file_name = spl_message[1].replace('\x05\r\n','')
#                             file_name = file_name.replace(' ','')
#                             # Выделяем имя файла и записываем его в словарь со значением False
#                             if file_name.__contains__('.') == True:
#                                 _files[file_name] = {'loaded': False, 'isInArchive': False}
                        
#                         if message.__contains__('╘рщы яюьх∙хэ т т√їюфэющ ЁхёєЁё (file://C:\oev\exg\\rcv)'):
#                             # Если сообщение содержит -> Файл помещен в выходной ресурс ...
#                             spl_message = message.split(':')
#                             file_name = spl_message[0]
#                             # Обновляем словарь по имени файла(ключу), записываем значение True -> Файл успешно загрузился на ресурс
#                             try:
#                                 if file_name.__contains__('.') == True:
#                                     _files[file_name]['loaded'] = True
#                             except KeyError:
#                                 print("Нет такого файла в списке")

#             except UnicodeDecodeError as ex:
#                 pass
        
#         #  Добавляем в конечный массив просмотра файлов, для последующей обработки
#         file_names_from_log.append(_files)
#         log.close()

# # print(file_names_from_log)

# """ Получаем имена фалов с архива """

# current_date = datetime.now().strftime("%d%m%Y")

# rcv = dir_armkbr + "\\Exg\\rcv\\1"
# bvp = rcv + "\\211"
# arc_dir = dir_archive + "\\" + datetime.now().strftime("%d.%m.%Y") + "\\uarm3\\inc\\ed"

# fe.check_dir(rcv)
# fe.check_dir(bvp)
# fe.check_dir(arc_dir)

# # fe.check_dir()

# arc_dirs = [rcv, bvp]
# xml_dir = [arc_dir,]

# file_names_from_archive = []
# file_names_from_archive_xml = []


# for _dir in arc_dirs:
#     files = {}
#     for file_name in os.listdir(_dir):
#         file_path = _dir + "\\" + file_name
#         if os.path.isfile(file_path) and file_name.__contains__('.') == True:
#             files[file_name] = {'isInLog': False, 'loaded': False, 'decode_vers': False}

#     file_names_from_archive.append(files)

# for _dir in xml_dir:
#     files = {}
#     for file_name in os.listdir(_dir):
#         file_path = _dir + "\\" + file_name
#         if os.path.isfile(file_path) and file_name.__contains__('.') == True:
#             files[file_name] = {'loaded': False, 'not_decode_vers': False}

#     file_names_from_archive_xml.append(files)

# # print(file_names_from_archive)

# """ Производим сверку """

# print('\n')

# for xml_dict in file_names_from_archive_xml:
#     for xml_k, xml_v in xml_dict.items():
#         for arc_dict in file_names_from_archive:
#             for ak, av in arc_dict.items():
#                 try:
#                     if xml_k[:-4].lower() == ak.lower():
#                         arc_dict[ak]['decode_vers'] = True
#                         xml_dict[xml_k]['not_decode_vers'] = True
#                 except KeyError as ex:
#                     print('Ошибка ключа')

# xml_count = 0
# for xml_dict in file_names_from_archive_xml:
#     for xml_k, xml_v in xml_dict.items():
#         if xml_v['not_decode_vers'] == False:
#             print('Нет нерасширофанной версии файла {}'.format(xml_k))
#             xml_count += 1
# count = 0
# for arc_dict in file_names_from_archive:
#     for ak, av in arc_dict.items():
#         if av['decode_vers'] == False:
#             print('Нет расширофанной версии файла {}'.format(ak))
#             count += 1

# if count == 0 and xml_count == 0:
#     print('Архив расшифрованных и нерасшифрованных совпадают.')



# for arc_dict in file_names_from_archive:
#     for ak, av in arc_dict.items():
#         for log_dict in file_names_from_log:
#             try:
#                 if ak in log_dict:
#                     arc_dict[ak]['isInLog'] = True
#                     arc_dict[ak]['loaded'] = log_dict[ak]['loaded']
#                     log_dict[ak]['isInArchive'] = True

#             except KeyError as ex:
#                 print("Ошибка ключа")


# # print(file_names_from_log)
# # print(file_names_from_archive)

# log_count = 0
# for _dict in  file_names_from_log:
#     for k,v in _dict.items():
#         if v['loaded'] and v['isInArchive']:
#             log_count += 1
#         else:
#             message = ''
#             if v['loaded'] == False:
#                 message += '{} не был отправлен '.format(k)
#             if v['isInArchive'] == False:
#                 if message != '':
#                     message += ' и не был найден в архивах'
#                 else:
#                     message += '{} не был найден в архивах'.format(k)

#             print(message)
# arc_count = 0
# for _dict in  file_names_from_archive:
#     for k,v in _dict.items():
#         if v['loaded'] and v['isInLog']:
#             arc_count += 1
#         else:
#             message = ''
#             if v['loaded'] == False:
#                 message += '{} не был отправлен '.format(k)
#             if v['isInLog'] == False:
#                 if message != '':
#                     message += 'и не был найден в логах'
#                 else:
#                     message += '{} не был найден в логах'.format(k)

#             print(message)

# if log_count == arc_count:
#     print("Успешно отправленных файлов {}".format(log_count))
# else:
#     print("Расхождение в количестве отправленных документов лог -> {}, arch -> {}".format(log_count, arc_count))