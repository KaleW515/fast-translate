from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMainWindow, QMessageBox

import ui.Ui_about as Ui_about
from core.constants.notification import Notification
from core.utils import version


class UiAbout(QMainWindow, Ui_about.Ui_About):
    def __init__(self, parent=None):
        super(UiAbout, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.versionLabel.setText("v" + version.VERSION)
        self.checkUpdateButton.clicked.connect(self.__on_check_update_clicked)

    def __on_check_update_clicked(self):
        if not version.check_update():
            QMessageBox.information(self, Notification.SUCCESS_HEAD,
                                    Notification.HAVE_NO_NEW_VERSION_BODY)
        else:
            QMessageBox.information(self, Notification.FAIL_HEAD,
                                    Notification.HAVE_NEW_VERSION_BODY)
