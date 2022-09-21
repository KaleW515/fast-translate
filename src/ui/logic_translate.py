import asyncio
import logging
import time
from multiprocessing import Process

from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMainWindow

import container
import ui.Ui_translate as Ui_translate
from api import translator
from api.instant_translate import InstantTranslate

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
    start_translate_thread = pyqtSignal(name="start_translate_thread")

    def __init__(self, parent=None):
        super(UiTranslate, self).__init__(parent)
        self.setupUi(self)
        # 默认打开谷歌翻译国内源
        self.googleCNBox.setCheckState(Qt.Checked)
        self.translateButton.clicked.connect(self.on_translate_button_click)

        # 设置为未选中状态
        self.baiduBox.setCheckState(Qt.Unchecked)
        self.baiduText.setVisible(False)
        self.baiduLabel.setVisible(False)
        self.googleBox.setCheckState(Qt.Unchecked)
        self.googleText.setVisible(False)
        self.googleLable.setVisible(False)

        self.baiduBox.clicked.connect(self.on_baidubox_click)
        self.googleBox.clicked.connect(self.on_googlebox_click)
        self.googleCNBox.clicked.connect(self.on_googlecnbox_click)
        self.translateNowBox.clicked.connect(self.on_translatenowbox_click)

        self.fill_targetbox()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        # 设置线程相关
        self.translate_thread = TranslateThread()
        self.thread = QThread(self)
        self.translate_thread.moveToThread(self.thread)
        self.start_translate_thread.connect(self.translate_thread.run)
        self.translate_thread.baidu_signal.connect(self.baidu_res_set)
        self.translate_thread.google_signal.connect(self.google_res_set)
        self.translate_thread.googlecn_signal.connect(self.googlecn_res_set)

        # 设置即时翻译
        self.instantTranslateMode.currentTextChanged.connect(self.on_set_mode)
        self.it = None
        self.it_process = None

        # 菜单栏点击事件
        self.translateSetting.triggered.connect(self.on_translate_setting)
        self.aboutSetting.triggered.connect(self.on_about_setting)

        # 下面会用到的变量
        self.clipboard = container.get_container().clipboard
        self.ui_preference = container.get_container().ui_preference
        self.ui_about = container.get_container().ui_about

    # 窗口关闭事件
    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def on_translate_setting(self):
        self.ui_preference.show()

    def on_about_setting(self):
        self.ui_about.show()

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

    def googlecn_res_set(self, res):
        if self.additionalBox.isChecked():
            self.googleCNText.setPlainText(self.googleCNText.toPlainText() + res)
        else:
            self.googleCNText.setPlainText(res)

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
            if self.it is not None:
                self.it.release_key()
            if self.it_process is not None:
                self.it_process.terminate()
                self.it_process.join()
            logging.info("it_process is stopped")

    def on_baidubox_click(self):
        self.baiduLabel.setVisible(self.baiduBox.isChecked())
        self.baiduText.setVisible(self.baiduBox.isChecked())

    def on_googlebox_click(self):
        self.googleLable.setVisible(self.googleBox.isChecked())
        self.googleText.setVisible(self.googleBox.isChecked())

    def on_googlecnbox_click(self):
        self.googleCNLable.setVisible(self.googleCNBox.isChecked())
        self.googleCNText.setVisible(self.googleCNBox.isChecked())

    def on_translate_button_click(self):
        self.clipboard.setText(self.originalText.toPlainText())

    def on_translatenowbox_click(self):
        if self.translateNowBox.isChecked():
            if self.instantTranslateMode.currentText() == "MODE 0":
                self.it = InstantTranslate()
                self.it.release_key()
                self.it_process = Process(target=self.it.run)
                self.it_process.start()
                logging.info("translate now box is checked")
            else:
                if self.it is not None:
                    self.it.release_key()
                    self.it = None
                if self.it_process is not None:
                    self.it_process.terminate()
                    self.it_process.join()
                    self.it_process = None
                logging.info("translate now process is stopped")
        else:
            # 停止it_process进程
            if self.it is not None:
                self.it.release_key()
                self.it = None
            logging.info("translate thread release key")
            if self.it_process is not None:
                self.it_process.terminate()
                self.it_process.join()
                self.it_process = None
            logging.info("translate now process is stopped")

    def on_set_mode(self):
        logging.info("now mode is {}".format(self.instantTranslateMode.currentText()))
        self.on_translatenowbox_click()

    def fill_targetbox(self):
        targets = container.get_container().config.target_list
        self.targetBox.addItems(targets)
        self.instantTranslateMode.addItems({"MODE 0": 0, "MODE 1": 1})

    def get_curr_server(self):
        curr_server = set()
        if self.baiduBox.isChecked():
            curr_server.add("baidu")
        if self.googleBox.isChecked():
            curr_server.add("google")
        if self.googleCNBox.isChecked():
            curr_server.add("googlecn")
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
    googlecn_signal = pyqtSignal(str, name="googlecn_signal")

    def __init__(self):
        super(TranslateThread, self).__init__()
        self.tasks = []
        self.loop = asyncio.new_event_loop()
        self.cfg = container.get_container().config
        self.trans_object = translator.Translator()

    async def do_translate(self, original, server: str, text_to):
        res, success = await self.trans_object.translate(original, server, text_to)
        print("server: {}, res: {}".format(server, res))
        if server == "baidu":
            self.baidu_signal.emit(res)
        if server == "google":
            self.google_signal.emit(res)
        if server == "googlecn":
            self.googlecn_signal.emit(res)

    # 停止协程
    def stop_coroutine(self):
        for task in self.tasks:
            task.cancel()
        self.loop.stop()

    def run(self):
        main_window = container.get_container().main_window
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.tasks = []
        server = set()
        for task in self.tasks:
            task.cancel()
        if main_window.baiduBox.isChecked():
            self.tasks.append(
                self.loop.create_task(
                    self.do_translate(now["original"], "baidu", self.cfg.baidu_target[now["target"]])))
            server.add("baidu")
        if main_window.googleBox.isChecked():
            self.tasks.append(
                self.loop.create_task(
                    self.do_translate(now["original"], "google", self.cfg.google_target[now["target"]])))
            server.add("google")
        if main_window.googleCNBox.isChecked():
            self.tasks.append(
                self.loop.create_task(
                    self.do_translate(now["original"], "googlecn", self.cfg.googlecn_target[now["target"]])))
            server.add("googlecn")
        self.loop.run_until_complete(asyncio.wait(self.tasks, return_when=asyncio.FIRST_EXCEPTION))
        cache["server"] = now["server"]
        cache["original"] = now["original"]
        cache["target"] = now["target"]


def clipboard_change():
    clipboard = container.get_container().clipboard
    is_selection = clipboard.Clipboard
    main_window = container.get_container().main_window
    if main_window.instantTranslateMode.currentText() == "MODE 1" and main_window.translateNowBox.isChecked():
        is_selection = clipboard.Selection
    data = clipboard.mimeData(is_selection)
    target = main_window.get_curr_target()
    server = main_window.get_curr_server()
    if data.text() == cache["original"] and target == cache["target"] and server == cache["server"]:
        pass
    else:
        if 'text/uri-list' in data.formats() or 'application/x-qt-image' in data.formats():
            pass
        else:
            original = data.text()
            main_window.set_original_text(original)
            if main_window.isHidden():
                main_window.show()
            now["original"] = original
            now["target"] = target
            now["server"] = server
            global last_time
            if time.time() - last_time < 1:
                time.sleep(1)
            if main_window.originalText.toPlainText() == original:
                last_time = time.time()
                main_window.start_translate_thread.emit()
            else:
                last_time = time.time()
                main_window.start_translate_thread.emit()


last_time = time.time()
