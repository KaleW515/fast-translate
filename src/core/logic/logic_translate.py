import asyncio
import logging
from multiprocessing import Process

from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMainWindow

import container
import ui.Ui_translate as Ui_translate
from core.constants.translator_enums import TranslatorEnums
from core.translate import translator
from core.translate.instant_translate import InstantTranslate
from core.utils import log

cache = {
    "original": "",
    "result": "",
    "server": set(),
    "target": []
}

curr = {
    "original": "",
    "result": "",
    "server": set(),
    "target": []
}

logging.basicConfig(level=log.get_log_config()[0], filename=log.get_log_config()[1],
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


class UiTranslate(QMainWindow, Ui_translate.Ui_MainWindow):
    start_translate_thread = pyqtSignal(bool, name="start_translate_thread")

    def __init__(self, parent=None):
        super(UiTranslate, self).__init__(parent)
        self.setupUi(self)
        # 默认打开百度翻译国内源
        self.baiduBox.setCheckState(Qt.Checked)
        # 翻译按钮点击事件
        self.translateButton.clicked.connect(self.__on_translate_button_click)

        # 设置为未选中状态
        self.googleCNBox.setCheckState(Qt.Unchecked)
        self.googleCNText.setVisible(False)
        self.googleCNLable.setVisible(False)
        self.googleBox.setCheckState(Qt.Unchecked)
        self.googleText.setVisible(False)
        self.googleLable.setVisible(False)

        self.baiduBox.clicked.connect(self.__on_baidubox_click)
        self.googleBox.clicked.connect(self.__on_googlebox_click)
        self.googleCNBox.clicked.connect(self.__on_googlecnbox_click)
        self.translateNowBox.clicked.connect(self.__on_translatenowbox_click)

        self.__fill_targetbox()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        # 设置线程相关
        self.translate_thread = TranslateThread()
        self.thread = QThread(self)
        self.translate_thread.moveToThread(self.thread)
        self.start_translate_thread.connect(self.translate_thread.run)
        self.translate_thread.baidu_signal.connect(self.__baidu_res_set)
        self.translate_thread.google_signal.connect(self.__google_res_set)
        self.translate_thread.googlecn_signal.connect(self.__googlecn_res_set)

        # 设置即时翻译
        self.it = None
        self.it_process = None

        # 菜单栏点击事件
        self.translateSetting.triggered.connect(self.__on_translate_setting)
        self.aboutSetting.triggered.connect(self.__on_about_setting)
        self.copykeySetting.triggered.connect(self.__on_copykey_setting)

        # 下面会用到的变量
        self.clipboard = container.get_container().clipboard
        self.ui_preference = container.get_container().ui_preference
        self.ui_about = container.get_container().ui_about
        self.ui_copykey = container.get_container().ui_copykey

    # 窗口关闭事件
    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def __on_translate_setting(self):
        self.ui_preference.show()
        self.ui_preference.do_fill_secrets()

    def __on_about_setting(self):
        self.ui_about.show()

    def __on_copykey_setting(self):
        self.ui_copykey.show()
        self.ui_copykey.run_listener()
        self.ui_copykey.do_fill_text()

    def __baidu_res_set(self, res):
        if self.additionalBox.isChecked():
            self.baiduText.setPlainText(self.baiduText.toPlainText() + res)
        else:
            self.baiduText.setPlainText(res)

    def __google_res_set(self, res):
        if self.additionalBox.isChecked():
            self.googleText.setPlainText(self.googleText.toPlainText() + res)
        else:
            self.googleText.setPlainText(res)

    def __googlecn_res_set(self, res):
        if self.additionalBox.isChecked():
            self.googleCNText.setPlainText(self.googleCNText.toPlainText() + res)
        else:
            self.googleCNText.setPlainText(res)

    def stop_thread(self):
        if not self.thread.isRunning():
            logging.debug("translate thread is not running")
            return
        else:
            logging.debug("translate thread is running")
            self.thread.quit()
            self.thread.wait()
            logging.debug("translate thread is stopped")

    def stop_process(self):
        if self.it_process is None:
            logging.debug("translate now process is not running")
            return
        if not self.it_process.is_alive():
            logging.debug("it_process is not alive")
            return
        else:
            logging.debug("it_process is alive")
            if self.it is not None:
                self.it.release_key()
            if self.it_process is not None:
                self.it_process.terminate()
                self.it_process.join()
            logging.debug("it_process is stopped")

    def __on_baidubox_click(self):
        self.baiduLabel.setVisible(self.baiduBox.isChecked())
        self.baiduText.setVisible(self.baiduBox.isChecked())

    def __on_googlebox_click(self):
        self.googleLable.setVisible(self.googleBox.isChecked())
        self.googleText.setVisible(self.googleBox.isChecked())

    def __on_googlecnbox_click(self):
        self.googleCNLable.setVisible(self.googleCNBox.isChecked())
        self.googleCNText.setVisible(self.googleCNBox.isChecked())

    def __on_translate_button_click(self):
        self.clipboard.setText(self.originalText.toPlainText().strip())
        self.start_translate_thread.emit(False)

    def __on_translatenowbox_click(self):
        if self.translateNowBox.isChecked():
            self.__do_release_it_process()
            self.it = InstantTranslate()
            self.it.release_key()
            self.it_process = Process(target=self.it.run)
            self.it_process.start()
            logging.debug("translate now box is checked")
        else:
            self.__do_release_it_process()

    def __do_release_it_process(self):
        # 停止it_process进程
        if self.it is not None:
            self.it.release_key()
            self.it = None
            logging.debug("translate thread release key")
        if self.it_process is not None:
            self.it_process.terminate()
            self.it_process.join()
            self.it_process = None
            logging.debug("translate now process is stopped")

    def __fill_targetbox(self):
        targets = container.get_container().config.target_list
        self.targetBox.addItems(targets)

    def get_curr_server(self):
        curr_server = set()
        if self.baiduBox.isChecked():
            curr_server.add(TranslatorEnums.BAIDU)
        if self.googleBox.isChecked():
            curr_server.add(TranslatorEnums.GOOGLE)
        if self.googleCNBox.isChecked():
            curr_server.add(TranslatorEnums.GOOGLECN)
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
    signal_suffix = "_signal"
    baidu_signal = pyqtSignal(str, name=TranslatorEnums.BAIDU.name + signal_suffix)
    google_signal = pyqtSignal(str, name=TranslatorEnums.GOOGLE.name + signal_suffix)
    googlecn_signal = pyqtSignal(str, name=TranslatorEnums.GOOGLECN.name + signal_suffix)

    def __init__(self):
        super(TranslateThread, self).__init__()
        self.tasks = []
        self.loop = asyncio.new_event_loop()
        self.cfg = container.get_container().config
        self.trans_object = translator.Translator()

    async def __do_translate(self, original, server, text_to, use_cache: bool):
        res, success = await self.trans_object.translate(original, server, text_to, use_cache)
        logging.info("server: {}, res: {}".format(server, res))
        if server == TranslatorEnums.BAIDU:
            self.baidu_signal.emit(res)
        if server == TranslatorEnums.GOOGLE:
            self.google_signal.emit(res)
        if server == TranslatorEnums.GOOGLECN:
            self.googlecn_signal.emit(res)

    # 停止协程
    def stop_coroutine(self):
        for task in self.tasks:
            task.cancel()
        self.loop.stop()

    def __do_clean_tasks(self):
        tasks = []
        for task in self.tasks:
            if not task.done():
                tasks.append(task)
        self.tasks = tasks

    def run(self, use_cache: bool):
        main_window = container.get_container().main_window
        server = set()
        # 清理过期任务
        self.__do_clean_tasks()
        if main_window.baiduBox.isChecked():
            self.tasks.append(
                self.loop.create_task(
                    self.__do_translate(curr["original"], TranslatorEnums.BAIDU,
                                        self.cfg.baidu_target[curr["target"]], use_cache)))
            server.add(TranslatorEnums.BAIDU)
        if main_window.googleBox.isChecked():
            self.tasks.append(
                self.loop.create_task(
                    self.__do_translate(curr["original"], TranslatorEnums.GOOGLE,
                                        self.cfg.google_target[curr["target"]], use_cache)))
            server.add(TranslatorEnums.GOOGLE)
        if main_window.googleCNBox.isChecked():
            self.tasks.append(
                self.loop.create_task(
                    self.__do_translate(curr["original"], TranslatorEnums.GOOGLECN,
                                        self.cfg.googlecn_target[curr["target"]], use_cache)))
            server.add(TranslatorEnums.GOOGLECN)
        self.loop.run_until_complete(asyncio.wait(self.tasks, return_when=asyncio.FIRST_EXCEPTION))
        cache["server"] = curr["server"]
        cache["original"] = curr["original"]
        cache["target"] = curr["target"]


def clipboard_change():
    clipboard = container.get_container().clipboard
    if not container.get_container().main_window.isMinimized():
        submit_translate(clipboard.mimeData(clipboard.Clipboard))


def submit_translate(data):
    main_window = container.get_container().main_window
    target = main_window.get_curr_target()
    server = main_window.get_curr_server()
    if data.text() == cache["original"] and target == cache["target"] and server == cache["server"]:
        pass
    else:
        if 'text/uri-list' in data.formats() or 'application/x-qt-image' in data.formats():
            pass
        else:
            original = data.text()
            main_window.set_original_text(" " + original)
            curr["original"] = original
            curr["target"] = target
            curr["server"] = server
            main_window.start_translate_thread.emit(True)
