import sys
import logging

def get_log_config():
    dev = False
    if len(sys.argv) > 1:
        if sys.argv[1] == "dev":
            dev = True
    level = logging.DEBUG
    filename = None
    if dev:
        level = logging.WARN
        # filename = "../log/ft.log"
        filename = None
    return level, filename