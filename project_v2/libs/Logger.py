from datetime import datetime
import logging


class Logger:
    def __init__(self, file_log_path=None, form_log_path=None):
        if form_log_path is not None:
            self.form_log = form_log_path

        # logging.basicConfig(filename=logTo + '\\1\\' + datetime.now().strftime("%Y%m%d") + '\\' + "sample.log", level=logging.INFO)

    def log(self, message, isError=False):
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if isError:
            self.form_log.append("<font color='red'>{date} {message}</font>".format(date=current_datetime, message=message))
        else:
            self.form_log.append("<font color='white'>{date} {message}</font>".format(date=current_datetime, message=message))

