from time import sleep
from datetime import datetime
import logging
from threading import Thread
from PyQt5 import QtWidgets, QtCore, QtGui

from libs.FileExplorer import FileExplorer

from contants.path_constants import puds_disk, dir_log
from libs.LogType import LogType


class Logger(QtCore.QObject):

    def __init__(self, file_log_path=None, form_log_path=None):
        fe = FileExplorer()

        fe.check_dir(file_log_path + "\\1\\" +
                     datetime.now().strftime("%Y%m%d") + "\\")

        if form_log_path is not None:
            self.form_log = form_log_path

        self.file_log_path = file_log_path

        if self.file_log_path != None:
            self.visual = self.setup_logger(name="visuallogger", log_file="{}\\1\\{}\\visual.log".format(file_log_path,datetime.now().strftime("%Y%m%d")))

            self.back = self.setup_logger("backlogger", "{}\\1\\{}\\sample.log".format(file_log_path,datetime.now().strftime("%Y%m%d")))

    def setup_logger(self,name, log_file, level=logging.INFO):
        """To setup as many loggers as you want"""

        handler = logging.FileHandler(log_file)
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)

        return logger

    def log(self, message, log_type: LogType.DEBUG):
        """Функция логирования, со своими фичами"""
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        current_datetime_mls = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

        if log_type == LogType.DEBUG:
            if self.file_log_path is not None:
                self.back.info("INFO|{}|{}".format(
                    current_datetime_mls, message))

        elif log_type == LogType.FILES:
            if self.file_log_path is not None:
                self.form_log.append(
                    "<font color='green'>{message}</font>".format(
                        date=current_datetime, message=message
                    )
                )
                self.back.info("FILES|{}|{}".format(
                    current_datetime_mls, message))
                self.visual.info("FILES|{}|{}".format(
                current_datetime_mls, message))

        elif log_type == LogType.INFO:
            if message == "" or message == " ":
                self.form_log.append("")
            else:
                self.form_log.append(
                    "<font color='white'>{date} {message}</font>".format(
                        date=current_datetime, message=message
                    )
                )
            if self.file_log_path is not None:
                self.visual.info("INFO|{}|{}".format(current_datetime_mls, message))
                self.back.info("INFO|{}|{}".format(current_datetime_mls, message))

        elif log_type == LogType.ERROR:
            if message == "" or message == " ":
                self.form_log.append("")
            else:
                self.form_log.append(
                    "<font color='red'>{date} {message}</font>".format(
                        date=current_datetime, message=message
                    )
                )

            if self.file_log_path is not None:
                self.back.error("ERROR|{}|{}".format(
                    current_datetime_mls, message), stack_info=True)
                self.visual.error("ERROR|{}|{}".format(
                    current_datetime_mls, message))

        elif log_type == LogType.WARNING:
            if message == "" or message == " ":
                self.form_log.append("")
            else:
                self.form_log.append(
                    "<font color='orange'>{date} {message}</font>".format(
                        date=current_datetime, message=message
                    )
                )

            if self.file_log_path is not None:
                self.back.warning("WARNING|{}|{}".format(
                    current_datetime_mls, message))
                self.visual.warning("WARNING|{}|{}".format(
                    current_datetime_mls, message))

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
            self.logger.log("CheckConnectionn", LogType.DEBUG)

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
                    + "\\",filter='sample.log',
                    name_of_doc='log'
                )
                fe.copy_files(
                    path_from=curr_log,
                    path_to=puds_disk
                    + "LOGS_FOR_SEND_MESSAGE\\"
                    + currentDate.strftime("%Y%m%d")
                    + "\\",filter='sample.log',
                    name_of_doc='log'
                )

                self.prev_log = curr_log
            else:
                fe.copy_files(
                    path_from=curr_log,
                    path_to=puds_disk
                    + "LOGS_FOR_SEND_MESSAGE\\"
                    + currentDate.strftime("%Y%m%d")
                    + "\\",filter='sample.log',
                    name_of_doc='log'
                )

            sleep(240)
