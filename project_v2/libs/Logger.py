from time import sleep
from datetime import datetime
import logging
from threading import Thread

# from PyQt5.qtread import Thread

from PyQt5 import QtWidgets, QtCore, QtGui

from libs.FileExplorer import FileExplorer

from contants.path_constants import puds_disk, dir_log


class Logger(QtCore.QObject):
    def __init__(self, file_log_path=None, form_log_path=None):
        fe = FileExplorer()

        fe.check_dir(file_log_path + "\\1\\" + datetime.now().strftime("%Y%m%d") + "\\")

        if form_log_path is not None:
            self.form_log = form_log_path

        self.file_log_path = file_log_path

        if self.file_log_path != None:
            logging.basicConfig(
                filename=file_log_path
                + "\\1\\"
                + datetime.now().strftime("%Y%m%d")
                + "\\"
                + "sample.log",
                level=logging.INFO,
            )

    def log(self, message, isError=False, onlyInFile=False):
        """Функция логирования, со своими фичами"""
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        current_datetime_mls = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

        if isError:
            if onlyInFile == False:
                if message == "" or message == " ":
                    self.form_log.append("")
                else:
                    self.form_log.append(
                        "<font color='red'>{date} {message}</font>".format(
                            date=current_datetime, message=message
                        )
                    )

            if self.file_log_path is not None:
                logging.error("|{}|{}".format(current_datetime_mls, message))

        else:
            if onlyInFile == False:
                if message == "" or message == " ":
                    self.form_log.append("")
                else:
                    self.form_log.append(
                        "<font color='white'>{date} {message}</font>".format(
                            date=current_datetime, message=message
                        )
                    )

            if self.file_log_path is not None:
                logging.info("|{}|{}".format(current_datetime_mls, message))


class CheckConnection(Thread):
    def __init__(self, log_path, _logger):
        Thread.__init__(self)
        self.work = True
        self.log_path = log_path
        self.logger = _logger

    def run(self):
        fe = FileExplorer()
        self.prev_log = (
            self.log_path + "\\1\\" + datetime.now().strftime("%Y%m%d") + "\\"
        )
        while self.work:
            print("checkConnection")
            currentDate = datetime.now()
            self.logger.log("CheckConnectionn", onlyInFile=True)

            curr_log = self.log_path + "\\1\\" + currentDate.strftime("%Y%m%d")

            fe.check_dir(
                puds_disk
                + "LOGS_FOR_SEND_MESSAGE\\"
                + currentDate.strftime("%Y%m%d")
                + "\\"
            )

            if self.prev_log != curr_log:

                fe.copy_files(
                    path_from=self.prev_log,
                    path_to=puds_disk
                    + "LOGS_FOR_SEND_MESSAGE\\"
                    + currentDate.strftime("%Y%m%d")
                    + "\\",
                )
                fe.copy_files(
                    path_from=curr_log,
                    path_to=puds_disk
                    + "LOGS_FOR_SEND_MESSAGE\\"
                    + currentDate.strftime("%Y%m%d")
                    + "\\",
                )

                self.prev_log = curr_log
            else:
                fe.copy_files(
                    path_from=curr_log,
                    path_to=puds_disk
                    + "LOGS_FOR_SEND_MESSAGE\\"
                    + currentDate.strftime("%Y%m%d")
                    + "\\",
                )

            sleep(240)
