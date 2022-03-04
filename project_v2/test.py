from asyncio.log import logger
import os
import subprocess

from libs.Logger import Logger
from libs.LogType import LogType

logger = Logger("B:\\MCI\\LOG")

logger.log("Debug ", log_type=LogType.DEBUG)