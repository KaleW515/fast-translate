import ui.Ui_preference as Ui_preference
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import *
from utils import config_tools

class UiPreference(QMainWindow, Ui_preference.Ui_Preference):
    def __init__(self, parent=None):
        super(UiPreference, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        # 将baiduLink设置为文字链接
        self.baiduLink.setOpenExternalLinks(True)
        self.baiduLink.setText("<a href='https://github.com/KaleW515/fast-translate/blob/main/docs/百度翻译.md'>如何获取</a>")
        self.googleLink.setOpenExternalLinks(True)
        self.googleLink.setText("<a href='https://github.com/KaleW515/fast-translate/blob/main/docs/谷歌翻译.md'>如何填写</a>")
        self.baiduSaveButton.clicked.connect(self.on_baidu_save_clicked)
        self.baiduAppIdText.textEdited.connect(self.on_baidu_appid_appkey_text_edited)
        self.baiduAppKeyText.textEdited.connect(self.on_baidu_appid_appkey_text_edited)
        self.googleSaveButton.clicked.connect(self.on_google_save_clicked)
        self.googleProxyHeadText.textEdited.connect(self.on_google_protocol_proxy_text_edited)
        self.googleProxyTailText.textEdited.connect(self.on_google_protocol_proxy_text_edited)

    def on_baidu_save_clicked(self):
        app_id = self.baiduAppIdText.text()
        app_key = self.baiduAppKeyText.text()
        if app_id == "" or app_key == "":
            self.baiduSaveButton.setText("保存失败")
            self.baiduSaveButton.setStyleSheet("background-color: red")
            # 消息提示
            QMessageBox.warning(self, "提示", "请填写完整")
        else:
            if config_tools.change_baidu_secret(app_id, app_key):
                self.baiduSaveButton.setText("保存成功")
                self.baiduSaveButton.setStyleSheet("background-color: green")
            else:
                self.baiduSaveButton.setText("保存失败")
                self.baiduSaveButton.setStyleSheet("background-color: red")
                # 消息提示
                QMessageBox.warning(self, "提示", "保存失败")

    def on_baidu_appid_appkey_text_edited(self):
        if self.baiduSaveButton.text() == "保存失败":
            self.baiduSaveButton.setText("保存")
            self.baiduSaveButton.setStyleSheet("background-color: none")

    def on_google_save_clicked(self):
        protocol = self.googleProxyHeadText.text()
        proxy = self.googleProxyTailText.text()
        if protocol == "" or proxy == "":
            self.googleSaveButton.setText("保存失败")
            self.googleSaveButton.setStyleSheet("background-color: red")
            # 消息提示
            QMessageBox.warning(self, "提示", "请填写完整")
        else:
            if config_tools.change_google_proxy(protocol, proxy):
                self.googleSaveButton.setText("保存成功")
                self.googleSaveButton.setStyleSheet("background-color: green")
            else:
                self.googleSaveButton.setText("保存失败")
                self.googleSaveButton.setStyleSheet("background-color: red")
                # 消息提示
                QMessageBox.warning(self, "提示", "保存失败")

    def on_google_protocol_proxy_text_edited(self):
        if self.googleSaveButton.text() == "保存失败":
            self.googleSaveButton.setText("保存")
            self.googleSaveButton.setStyleSheet("background-color: none")


Preference = UiPreference()

def get_preference():
    return Preference