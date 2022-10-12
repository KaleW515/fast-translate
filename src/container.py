import logging
import sys

from PyQt5.QtWidgets import QApplication

from core.config import configuration
from core.logic.logic_preference import UiPreference


class Container:

    def __init__(self):
        self.app = None
        self.clipboard = None
        self.config = None
        self.main_window = None
        self.ui_preference = None
        self.ui_about = None

    def invoke_init(self):
        from core.logic.logic_translate import UiTranslate
        from core.logic.logic_about import UiAbout
        self.app = QApplication(sys.argv)
        self.clipboard = self.app.clipboard()
        self.config = configuration.Configuration()
        self.ui_preference = UiPreference()
        self.ui_about = UiAbout()
        self.main_window = UiTranslate()

        # self.do_logger_init()
        self.after_init()

    def after_init(self):
        from core.logic.logic_translate import clipboard_change
        self.clipboard.dataChanged.connect(clipboard_change)
        self.clipboard.selectionChanged.connect(clipboard_change)

    def do_logger_init(self):
        dev = False
        if len(sys.argv) > 1:
            if sys.argv[1] == "dev":
                dev = True
        level = logging.DEBUG
        filename = None
        if dev:
            level = logging.WARN
            filename = "../log/ft.log"
        logging.basicConfig(level=level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                            filename=filename)


container = None


def get_container():
    global container
    if container is None:
        container = Container()
    return container
