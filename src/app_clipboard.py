import sys

from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)
clipboard = app.clipboard()


def get_app_clipboard():
    return app, clipboard
