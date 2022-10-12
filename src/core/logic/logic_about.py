import ui.Ui_about as Ui_about
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import *
from core.utils import version


class UiAbout(QMainWindow, Ui_about.Ui_About):
    def __init__(self, parent=None):
        super(UiAbout, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.versionLabel.setText("v" + version.VERSION)
        self.checkUpdateButton.clicked.connect(self.on_check_update_clicked)

    def on_check_update_clicked(self):
        if not version.check_update():
            QMessageBox.information(self, "提示", "已经是最新版本")
        else:
            QMessageBox.information(self, "提示", "有新版本，请通过yay更新")

