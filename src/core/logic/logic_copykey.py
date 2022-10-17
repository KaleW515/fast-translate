import logging
import threading

from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from pynput import keyboard

import container
import ui.Ui_copykey as Ui_copykey
from core.constants.notification import Notification
from core.utils import log

logging.basicConfig(level=log.get_log_config()[0], filename=log.get_log_config()[1],
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


class UiCopykey(QMainWindow, Ui_copykey.Ui_Copykey):
    def __init__(self, parent=None):
        super(UiCopykey, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.copykeyResetButton.clicked.connect(self.__on_resetButton_click)
        self.copykeySaveButton.clicked.connect(self.__on_saveButton_click)

        self.lock = threading.Lock()
        self.listener = None
        self.keys = []
        self.trim_keys = []
        self.key_count = 0

    def closeEvent(self, event):
        if self.listener is not None:
            logging.debug("close window and set listener None")
            self.listener.stop()
            self.listener = None

    def __on_resetButton_click(self):
        self.copykeyTextLabel.setText("")
        if self.listener is None:
            logging.debug("reset keys")
            self.keys = []
            self.trim_keys = []
            self.copykeyTextLabel.setText("")
            self.run_listener()

    def __on_saveButton_click(self):
        if len(self.trim_keys) < 2:
            QMessageBox.warning(self, Notification.SUCCESS_HEAD, Notification.COPYKEY_LENGTH_SHORT)
            return

        save_result = container.get_container().config.save_copykey(self.trim_keys)
        if save_result:
            QMessageBox.information(self, Notification.SUCCESS_HEAD, Notification.SAVE_SUCCESS_BODY)
        else:
            QMessageBox.warning(self, Notification.FAIL_HEAD, Notification.SAVE_FAIL_BODY)

    def run_listener(self):
        self.listener = keyboard.Listener(on_press=self.__on_press, on_release=self.__on_release)
        self.listener.start()

    def __trim_key(self, key: str) -> str:
        return key.replace("'", "")

    def __on_press(self, key):
        if not self.keys:
            self.copykeyTextLabel.setText("")
        if key not in self.keys:
            try:
                self.lock.acquire()
                logging.debug("press key: {0}".format(key))
                target_key = self.__trim_key(key.__str__())
                self.keys.append(key)
                self.trim_keys.append(target_key)
                self.key_count += 1
                if self.copykeyTextLabel.text() == "":
                    self.copykeyTextLabel.setText(target_key)
                else:
                    self.copykeyTextLabel.setText(self.copykeyTextLabel.text() + " + " + target_key)
            finally:
                self.lock.release()

    def __on_release(self, key):
        if key in self.keys:
            try:
                self.lock.acquire()
                logging.debug("release {0}".format(key))
                self.key_count -= 1
                if self.key_count == 0:
                    logging.debug("stop this thread")
                    self.listener.stop()
                    self.listener = None
            finally:
                self.lock.release()

    def do_fill_text(self):
        keys = container.get_container().config.get_copykey()
        for key in keys:
            if self.copykeyTextLabel.text() == "":
                self.copykeyTextLabel.setText(str(key))
            else:
                self.copykeyTextLabel.setText(self.copykeyTextLabel.text() + " + " + str(key))
