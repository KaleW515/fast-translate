import logging
import sys

from core.constants.file_constants import FileConstants


def get_log_config():
    dev = False
    if len(sys.argv) > 1:
        if sys.argv[1] == "dev":
            dev = True
    level = logging.DEBUG
    filename = None
    if dev:
        level = logging.WARN
        filename = FileConstants.LOG_FILE_PATH
    return level, filename
