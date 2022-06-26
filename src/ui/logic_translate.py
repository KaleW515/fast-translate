import asyncio
import logging
from multiprocessing import Process

from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMainWindow

import app_clipboard
import ui.Ui_translate as Ui_translate
from api import translator
from api.instant_translate import InstantTranslate
from utils import config_tools
from ui import logic_preference, logic_about

cache = {
    "original": "",
    "result": "",
    "server": set(),
    "target": []
}

now = {
    "original": "",
    "result": "",
    "server": set(),
    "target": []
}

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class UiTranslate(QMainWindow, Ui_translate.Ui_MainWindow):
    start_translate_thread = pyqtSignal()

    def __init__(self, parent=None):
        super(UiTranslate, self).__init__(parent)
        self.setupUi(self)
        self.baiduBox.setCheckState(Qt.Checked)
        self.translateButton.clicked.connect(self.on_translate_button_click)
        # 设置为未选中状态
        self.googleBox.setCheckState(Qt.Unchecked)
        self.googleText.setVisible(False)
        self.googleLable.setVisible(False)

        self.baiduBox.clicked.connect(self.on_baidubox_click)
        self.googleBox.clicked.connect(self.on_googlebox_click)
        self.translateNowBox.clicked.connect(self.on_translatenowbox_click)
        self.fill_targetbox()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.translate_thread = TranslateThread()
        self.thread = QThread(self)
        self.translate_thread.moveToThread(self.thread)
        self.start_translate_thread.connect(self.translate_thread.run)
        self.translate_thread.baidu_signal.connect(self.baidu_res_set)
        self.translate_thread.google_signal.connect(self.google_res_set)

        self.targetBox.currentTextChanged.connect(clipboard_change)

        self.it = None
        self.it_process = None
        # 菜单栏点击事件
        self.translateSetting.triggered.connect(self.on_translate_setting)
        self.aboutSetting.triggered.connect(self.on_about_setting)

    def on_translate_setting(self):
        logic_preference.get_preference().show()

    def on_about_setting(self):
        logic_about.get_about().show()

    def baidu_res_set(self, res):
        if self.additionalBox.isChecked():
            self.baiduText.setPlainText(self.baiduText.toPlainText() + res)
        else:
            self.baiduText.setPlainText(res)

    def google_res_set(self, res):
        if self.additionalBox.isChecked():
            self.googleText.setPlainText(self.googleText.toPlainText() + res)
        else:
            self.googleText.setPlainText(res)

    def stop_thread(self):
        if not self.thread.isRunning():
            logging.info("translate thread is not running")
            return
        else:
            logging.info("translate thread is running")
            self.thread.quit()
            self.thread.wait()
            logging.info("translate thread is stopped")

    def stop_process(self):
        if self.it_process is None:
            logging.info("translate now process is not running")
            return
        if not self.it_process.is_alive():
            logging.info("it_process is not alive")
            return
        else:
            logging.info("it_process is alive")
            self.it.release_key()
            self.it_process.terminate()
            self.it_process.join()
            logging.info("it_process is stopped")

    def on_baidubox_click(self):
        self.baiduLabel.setVisible(self.baiduBox.isChecked())
        self.baiduText.setVisible(self.baiduBox.isChecked())

    def on_googlebox_click(self):
        self.googleLable.setVisible(self.googleBox.isChecked())
        self.googleText.setVisible(self.googleBox.isChecked())

    def on_translate_button_click(self):
        clipboard.setText(self.originalText.toPlainText())

    def on_translatenowbox_click(self):
        if self.translateNowBox.isChecked():
            self.it = InstantTranslate()
            self.it.release_key()
            self.it_process = Process(target=self.it.run)
            self.it_process.start()
            logging.info("translate now box is checked")
        else:
            # 停止it_process进程
            self.it.release_key()
            logging.info("translate thread release key")
            self.it_process.terminate()
            self.it_process.join()
            logging.info("translate now process is stopped")

    def fill_targetbox(self):
        targets = config_tools.get_config_constant()["targetList"]
        self.targetBox.addItems(targets)

    def get_curr_server(self):
        curr_server = set()
        if self.baiduBox.isChecked():
            curr_server.add("baidu")
        if self.googleBox.isChecked():
            curr_server.add("google")
        return curr_server

    def get_curr_target(self):
        curr_target = self.targetBox.currentText()
        return curr_target

    def set_original_text(self, text):
        if self.additionalBox.isChecked():
            self.originalText.setPlainText(self.originalText.toPlainText() + text)
        else:
            self.originalText.setPlainText(text)


class TranslateThread(QObject):
    baidu_signal = pyqtSignal(str, name="baidu_signal")
    google_signal = pyqtSignal(str, name="google_signal")

    def __init__(self):
        super(TranslateThread, self).__init__()
        self.tasks = []
        self.loop = asyncio.new_event_loop()
        self.cfg = config_tools.get_config_constant()
        self.transObject = translator.Translator()

    async def do_translate(self, original, server: str, text_to):
        res, success = await self.transObject.translate(original, server, text_to)
        print("server: {}, res: {}".format(server, res))
        if server == "baidu":
            self.baidu_signal.emit(res)
        if server == "google":
            self.google_signal.emit(res)

    # 停止协程
    def stop_coroutine(self):
        for task in self.tasks:
            task.cancel()
        self.loop.stop()

    def run(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.tasks = []
        server = set()
        for task in self.tasks:
            task.cancel()
        if MainWindow.baiduBox.isChecked():
            self.tasks.append(
                self.loop.create_task(
                    self.do_translate(now["original"], "baidu", self.cfg["baiduTarget"][now["target"]])))
            server.add("baidu")
        if MainWindow.googleBox.isChecked():
            self.tasks.append(
                self.loop.create_task(
                    self.do_translate(now["original"], "google", self.cfg["googleTarget"][now["target"]])))
            server.add("google")
        self.loop.run_until_complete(asyncio.wait(self.tasks, return_when=asyncio.FIRST_EXCEPTION))
        cache["server"] = now["server"]
        cache["original"] = now["original"]
        cache["target"] = now["target"]


def clipboard_change():
    data = clipboard.mimeData()
    target = MainWindow.get_curr_target()
    server = MainWindow.get_curr_server()
    if data.text() == cache["original"] and target == cache["target"] and server == cache["server"]:
        pass
    else:
        if 'text/uri-list' in data.formats() or 'application/x-qt-image' in data.formats():
            pass
        else:
            original = data.text()
            MainWindow.set_original_text(original)
            if MainWindow.isHidden():
                MainWindow.show()
            now["original"] = original
            now["target"] = target
            now["server"] = server
            MainWindow.start_translate_thread.emit()

MainWindow = UiTranslate()
_, clipboard = app_clipboard.get_app_clipboard()
clipboard.dataChanged.connect(clipboard_change)


def get_MainWindow():
    return MainWindow