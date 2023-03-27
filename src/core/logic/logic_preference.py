from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMainWindow, QMessageBox

import ui.Ui_preference as Ui_preference
from core.constants.links import Links
from core.constants.notification import Notification


class UiPreference(QMainWindow, Ui_preference.Ui_Preference):
    def __init__(self, parent=None):
        import container

        super(UiPreference, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        # 将baiduLink设置为文字链接
        self.baiduLink.setOpenExternalLinks(True)
        self.baiduLink.setText(Links.BAIDU_HELP_LINK)
        self.googleLink.setOpenExternalLinks(True)
        self.googleLink.setText(Links.GOOGLE_HELP_LINK)

        self.baiduSaveButton.clicked.connect(self.__on_baidu_save_clicked)
        self.baiduAppIdText.textEdited.connect(self.__on_baidu_appid_appkey_text_edited)
        self.baiduAppKeyText.textEdited.connect(self.__on_baidu_appid_appkey_text_edited)

        self.googleSaveButton.clicked.connect(self.__on_google_save_clicked)
        self.googleProxyHeadText.textEdited.connect(self.__on_google_protocol_proxy_text_edited)
        self.googleProxyTailText.textEdited.connect(self.__on_google_protocol_proxy_text_edited)

        self.redisSaveButton.clicked.connect(self.__on_redis_save_clicked)
        self.redisHostText.textEdited.connect(self.__on_redis_text_edited)
        self.redisPortText.textEdited.connect(self.__on_redis_text_edited)
        self.redisPasswordText.textEdited.connect(self.__on_redis_text_edited)

        self.config = container.get_container().config

    def __on_baidu_save_clicked(self):
        app_id = self.baiduAppIdText.text()
        app_key = self.baiduAppKeyText.text()
        if app_id == "" or app_key == "":
            self.baiduSaveButton.setText(Notification.SAVE_FAIL_BODY)
            self.baiduSaveButton.setStyleSheet(Notification.BUTTON_BACKGROUND_FAIL)
            # 消息提示
            QMessageBox.warning(self, Notification.FAIL_HEAD, Notification.SECRET_NOT_COMPLETE)
        else:
            if self.config.change_baidu_secret(app_id, app_key):
                self.baiduSaveButton.setText(Notification.SAVE_SUCCESS_BODY)
                self.baiduSaveButton.setStyleSheet(Notification.BUTTON_BACKGROUND_SUCCESS)
            else:
                self.baiduSaveButton.setText(Notification.SAVE_FAIL_BODY)
                self.baiduSaveButton.setStyleSheet(Notification.BUTTON_BACKGROUND_FAIL)
                # 消息提示
                QMessageBox.warning(self, Notification.FAIL_HEAD, Notification.SAVE_FAIL_BODY)

    def __on_baidu_appid_appkey_text_edited(self):
        self.baiduSaveButton.setText(Notification.SAVE_BUTTON_TEXT)
        self.baiduSaveButton.setStyleSheet(Notification.BUTTON_BACKGROUND_NONE)

    def __on_google_save_clicked(self):
        protocol = self.googleProxyHeadText.text()
        proxy = self.googleProxyTailText.text()
        if protocol == "" or proxy == "":
            self.googleSaveButton.setText(Notification.SAVE_FAIL_BODY)
            self.googleSaveButton.setStyleSheet(Notification.BUTTON_BACKGROUND_FAIL)
            # 消息提示
            QMessageBox.warning(self, Notification.FAIL_HEAD, Notification.SECRET_NOT_COMPLETE)
        else:
            if self.config.change_google_proxy(protocol, proxy):
                self.googleSaveButton.setText(Notification.SAVE_SUCCESS_BODY)
                self.googleSaveButton.setStyleSheet(Notification.BUTTON_BACKGROUND_SUCCESS)
            else:
                self.googleSaveButton.setText(Notification.SAVE_FAIL_BODY)
                self.googleSaveButton.setStyleSheet(Notification.BUTTON_BACKGROUND_FAIL)
                # 消息提示
                QMessageBox.warning(self, Notification.FAIL_HEAD, Notification.SAVE_FAIL_BODY)

    def __on_google_protocol_proxy_text_edited(self):
        self.googleSaveButton.setText(Notification.SAVE_BUTTON_TEXT)
        self.googleSaveButton.setStyleSheet(Notification.BUTTON_BACKGROUND_NONE)

    def __on_redis_save_clicked(self):
        host = self.redisHostText.text()
        port = self.redisPortText.text()
        password = self.redisPasswordText.text()
        if host == "" or port == "":
            self.redisSaveButton.setText(Notification.SAVE_FAIL_BODY)
            self.redisSaveButton.setStyleSheet(Notification.BUTTON_BACKGROUND_FAIL)
            # 消息提示
            QMessageBox.warning(self, Notification.FAIL_HEAD, Notification.SECRET_NOT_COMPLETE)
        else:
            if self.config.change_redis_secret(host, port, password):
                self.redisSaveButton.setText(Notification.SAVE_SUCCESS_BODY)
                self.redisSaveButton.setStyleSheet(Notification.BUTTON_BACKGROUND_SUCCESS)
            else:
                self.redisSaveButton.setText(Notification.SAVE_FAIL_BODY)
                self.redisSaveButton.setStyleSheet(Notification.BUTTON_BACKGROUND_FAIL)
                # 消息提示
                QMessageBox.warning(self, Notification.FAIL_HEAD, Notification.SAVE_FAIL_BODY)

    def __on_redis_text_edited(self):
        self.redisSaveButton.setText(Notification.SAVE_BUTTON_TEXT)
        self.redisSaveButton.setStyleSheet(Notification.BUTTON_BACKGROUND_NONE)

    def __do_button_init(self):
        self.googleSaveButton.setText(Notification.SAVE_BUTTON_TEXT)
        self.googleSaveButton.setStyleSheet(Notification.BUTTON_BACKGROUND_NONE)
        self.baiduSaveButton.setText(Notification.SAVE_BUTTON_TEXT)
        self.baiduSaveButton.setStyleSheet(Notification.BUTTON_BACKGROUND_NONE)
        self.redisSaveButton.setText(Notification.SAVE_BUTTON_TEXT)
        self.redisSaveButton.setStyleSheet(Notification.BUTTON_BACKGROUND_NONE)

    def do_fill_secrets(self):
        self.__do_button_init()
        import container
        config = container.get_container().config
        baidu = config.get_baidu_secret()
        google = config.get_google_secret()
        redis = config.get_redis_secret()
        if baidu is not None:
            self.baiduAppIdText.setText(baidu.app_id)
            self.baiduAppKeyText.setText(baidu.app_key)
        if google is not None:
            if len(google.proxies.keys()) != 0:
                self.googleProxyHeadText.setText(google.proxies.keys().__iter__().__next__())
                self.googleProxyTailText.setText(google.proxies.values().__iter__().__next__())
        if redis is not None:
            self.redisHostText.setText(redis.host)
            self.redisPortText.setText(redis.port)
            self.redisPasswordText.setText(redis.password)
