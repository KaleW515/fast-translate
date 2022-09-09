import sys

from PyQt5.QtWidgets import QApplication

from config import configuration
from ui.logic_preference import UiPreference


class Container:

    def __init__(self):
        self.app = None
        self.clipboard = None
        self.config = None
        self.main_window = None
        self.ui_preference = None
        self.ui_about = None

    def invoke_init(self):
        from ui.logic_translate import UiTranslate
        from ui.logic_about import UiAbout
        self.app = QApplication(sys.argv)
        self.clipboard = self.app.clipboard()
        self.config = configuration.Configuration()
        self.ui_preference = UiPreference()
        self.ui_about = UiAbout()
        self.main_window = UiTranslate()

        self.after_init()



    def after_init(self):
        from ui.logic_translate import clipboard_change
        self.clipboard.dataChanged.connect(clipboard_change)
        self.clipboard.selectionChanged.connect(clipboard_change)

container = None

def get_container():
    global container
    if container is None:
        container = Container()
    return container
