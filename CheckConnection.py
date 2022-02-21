from ast import Try
import sys
from threading import Thread
from time import sleep
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import QObject
import os
import shutil
import datetime
import logging


class CheckConnection(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            logging.info('|' + datetime.datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S.%f") + '| CheckConnectionn')
            sleep(300)
