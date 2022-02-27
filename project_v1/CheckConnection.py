import shutil
from threading import Thread
from time import sleep
import datetime
import logging
import os
from path_constants import logTo


class CheckConnection(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.prev_log = None
        # self.curr_log = None

    def mapping_network_drives(self):
        os.system('set trans_disk=x:')
        os.system('set puds_disk=w:')
        os.system('net use %trans_disk% /delete /y')
        os.system('net use %puds_disk% /delete /y')
        os.system('net use x: \\\\10.48.4.241\\transportbanks 1!QQww /USER:10.48.4.241\\svc95004800')
        os.system('net use w: \\\\10.48.4.241\\transport 1!QQww /USER:10.48.4.241\\svc95004800')

    def run(self):
        self.prev_log = logTo + '\\1\\' + datetime.datetime.now().strftime("%Y%m%d") + "\\sample.log"
        while True:
            currentDate = datetime.datetime.now()
            logging.info('|' + datetime.datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S.%f") + '| CheckConnectionn')

            # self.mapping_network_drives()
            curr_log = logTo + '\\1\\' + currentDate.strftime("%Y%m%d") + "\\sample.log"
            if not os.path.exists('w:\\LOGS_FOR_SEND_MESSAGE\\'+ currentDate.strftime("%Y%m%d") + '\\'):
                os.makedirs('w:\\LOGS_FOR_SEND_MESSAGE\\'+ currentDate.strftime("%Y%m%d") + '\\')

            if self.prev_log != curr_log:
                shutil.copy2(logTo + '\\1\\' + currentDate.strftime("%Y%m%d") + '\\' + "sample.log", 'w:\\LOGS_FOR_SEND_MESSAGE\\'+ currentDate.strftime("%Y%m%d") + '\\')

                shutil.copy2(logTo + '\\1\\' + currentDate.strftime("%Y%m%d") + '\\' + "sample.log", 'w:\\LOGS_FOR_SEND_MESSAGE\\'+ currentDate.strftime("%Y%m%d") + '\\')

                self.prev_log = curr_log
            else:
                shutil.copy2(logTo + '\\1\\' + currentDate.strftime("%Y%m%d") + '\\' + "sample.log", 'w:\\LOGS_FOR_SEND_MESSAGE\\'+ currentDate.strftime("%Y%m%d") + '\\')
            sleep(300)
