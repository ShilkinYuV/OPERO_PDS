from datetime import datetime, timedelta
from PyQt5.QtCore import QThread
from PyQt5 import QtCore

from libs.FileExplorer import FileExplorer
from contants.path_constants import dir_archive, dir_armkbr
from libs.LogType import LogType


class MakeArchive(QThread):

    log_str = QtCore.pyqtSignal(str, LogType)

    def __init__(self, button, form):
        QThread.__init__(self)
        self.button = button
        self.fe = FileExplorer()
        self.fe.log_str.connect(form.log)

    def run(self):
        """Создание архива"""
        # Получаем вчерашний день
        yesterday_date = (datetime.today() - timedelta(days=1))
        vch_day = yesterday_date.day
        vch_month = yesterday_date.month
        vch_year = yesterday_date.year
        # Если число не 2ух значное, добавляем ноль в начале
        if vch_day.__str__().__len__() == 1:
            vch_day = "0{}".format(vch_day.__str__())
        else:
            vch_day = vch_day.__str__()

        if vch_month.__str__().__len__() == 1:
            vch_month = "0{}".format(vch_month.__str__())
        else:
            vch_month = vch_month.__str__()

        yesterday = "{}.{}.{}".format(vch_day, vch_month,vch_year)
        current_date = datetime.now().strftime("%d.%m.%Y")

        archive = dir_archive +  "\\{}\\uarm3\\inc\\ed\\".format(current_date)
        vchera= dir_archive + "\\{}\\uarm3\\inc\\ed\\".format(yesterday)
        self.fe.check_dir(vchera)

        rcv = dir_armkbr + "\\Exg\\rcv\\1"
        archrcv = dir_archive + "\\{}\\uarm3\\rcv".format(yesterday)
        self.fe.check_dir(archrcv)
        kvit= dir_archive + "\\{}\\uarm3\\квитанции\\".format(yesterday)
        self.fe.check_dir(kvit)

        self.fe.move_files(archive,vchera,filter=r'.*4525000987000000000000ED2114' + vch_day + r'.*\..*')
        self.fe.move_files(archive,vchera,filter=r'.*452500098700000000PacketEPD0' + vch_day + r'.*\..*')
        self.fe.move_files(archive,vchera,filter=r'.*452500098700000000PacketEPD4' + vch_day + r'.*\..*')
        self.fe.move_files(archive,vchera,filter=r'.*452500098700000000PacketEID0' + vch_day + r'.*\..*')
        self.fe.move_files(archive,vchera,filter=r'.*4525000987000000000000ED2450' + vch_day + r'.*\..*')
        self.fe.move_files(archive,vchera,filter=r'.*4525000987000000000000ED8024' + vch_day + r'.*\..*')
        self.fe.move_files(archive,vchera,filter=r'.*4525000987000000000000ED1014' + vch_day + r'.*\..*')
        self.fe.move_files(archive,vchera,filter=r'.*45250009870000000PacketESID0' + vch_day + r'.*\..*')
        self.fe.move_files(archive,vchera,filter=r'.*45250009870000000PacketESID4' + vch_day + r'.*\..*')
        self.fe.move_files(archive,vchera,filter=r'.*4525000987000000000000ED2050' + vch_day + r'.*\..*')
        self.fe.move_files(archive,vchera,filter=r'.*4525000987000000000000ED2010' + vch_day + r'.*\..*')
        self.fe.move_files(archive,vchera,filter=r'.*4525000987000000000000ED2410' + vch_day + r'.*\..*')
        self.fe.move_files(archive,vchera,filter=r'.*4525000987000000000000ED8080' + vch_day + r'.*\..*')
        self.fe.move_files(archive,vchera,filter=r'.*4525000987000000000000ED1044' + vch_day + r'.*\..*')
        self.fe.move_files(archive,vchera,filter=r'.*4525000987000000000000ED1054' + vch_day + r'.*\..*')
        self.fe.move_files(archive,vchera,filter=r'.*ED211' + vch_day + r'.*\..*')
        self.fe.move_files(archive,vchera,filter=r'.*ED808' + vch_day + r'.*\..*')

        self.fe.move_files(rcv,archrcv,filter=r'.*4525000987000000000000ED2114' + vch_day + r'.*\..*')
        self.fe.move_files(rcv,archrcv,filter=r'.*452500098700000000PacketEPD0' + vch_day + r'.*\..*')
        self.fe.move_files(rcv,archrcv,filter=r'.*452500098700000000PacketEPD4' + vch_day + r'.*\..*')
        self.fe.move_files(rcv,archrcv,filter=r'.*452500098700000000PacketEID0' + vch_day + r'.*\..*')
        self.fe.move_files(rcv,archrcv,filter=r'.*4525000987000000000000ED2450' + vch_day + r'.*\..*')
        self.fe.move_files(rcv,archrcv,filter=r'.*4525000987000000000000ED8024' + vch_day + r'.*\..*')
        self.fe.move_files(rcv,archrcv,filter=r'.*4525000987000000000000ED1014' + vch_day + r'.*\..*')
        self.fe.move_files(rcv,archrcv,filter=r'.*45250009870000000PacketESID0' + vch_day + r'.*\..*')
        self.fe.move_files(rcv,archrcv,filter=r'.*45250009870000000PacketESID4' + vch_day + r'.*\..*')
        self.fe.move_files(rcv,archrcv,filter=r'.*4525000987000000000000ED2050' + vch_day + r'.*\..*')
        self.fe.move_files(rcv,archrcv,filter=r'.*4525000987000000000000ED2010' + vch_day + r'.*\..*')
        self.fe.move_files(rcv,archrcv,filter=r'.*4525000987000000000000ED2410' + vch_day + r'.*\..*')
        self.fe.move_files(rcv,archrcv,filter=r'.*4525000987000000000000ED8080' + vch_day + r'.*\..*')
        self.fe.move_files(rcv,archrcv,filter=r'.*4525000987000000000000ED1044' + vch_day + r'.*\..*')
        self.fe.move_files(rcv,archrcv,filter=r'.*4525000987000000000000ED1054' + vch_day + r'.*\..*')
        self.fe.move_files(rcv,archrcv,filter=r'.*ED807' + vch_day + r'.*\..*')
        self.fe.move_files(rcv,archrcv,filter=r'.*ED330' + vch_day + r'.*\..*')
        self.fe.move_files(rcv,archrcv,filter=r'.*ED211' + vch_day + r'.*\..*')
        self.fe.move_files(rcv,archrcv,filter=r'.*ED808' + vch_day + r'.*\..*')

        

        self.button.setDisabled(False)