import json
import logging
import os
import shutil


class Configuration:

    def __init__(self):
        self.home_path = os.getenv("HOME")
        self.target_list = None
        self.baidu_target = None
        self.google_target = None
        self.googlecn_target = None

        self.baidu_app_id = None
        self.baidu_app_key = None
        self.google_proxies = None
        self.check_config()
        self.constant_init()
        self.secret_init()

    def constant_init(self):
        try:
            with open("./config/constants.json", "r") as f:
                cfg = json.load(f)
                self.target_list = cfg["targetList"]
                self.baidu_target = cfg["baiduTarget"]
                self.google_target = cfg["googleTarget"]
                self.googlecn_target = cfg["googleCNTarget"]
            logging.info("init constant success ~")
        except:
            raise IOError("parse constants.json failed, please check again ~")
        return


    def secret_init(self):
        try:
            with open(self.home_path + "/.config/fast-translate/config.json", "r") as f:
                cfg = json.load(f)
                if cfg["baiduSecret"]["appid"] != "":
                    self.baidu_app_id = cfg["baiduSecret"]["appid"]
                if cfg["baiduSecret"]["appKey"] != "":
                    self.baidu_app_key = cfg["baiduSecret"]["appKey"]
                if cfg["googleSecret"]["proxies"] != "":
                    self.google_proxies = cfg["googleSecret"]["proxies"]
            logging.info("init secret success ~")
        except:
            raise IOError("parse config.json failed, please check again ~")
        return


    def check_config(self):
        if not os.path.exists(self.home_path + "/.config"):
            os.mkdir(self.home_path + "/.config")
        if not os.path.exists(self.home_path + "/.config/fast-translate"):
            os.mkdir(self.home_path + "/.config/fast-translate")
        if not os.path.exists(self.home_path + "/.config/fast-translate/config.json"):
            # 将config_template.json复制到config.json
            shutil.copy("./config/config_template.json", self.home_path + "/.config/fast-translate/config.json")

    @staticmethod
    def refresh_config(func):
        def wrap(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self.check_config()
            self.constant_init()
            self.secret_init()
        return wrap

    def change_baidu_secret(self, appid: str, appkey: str):
        try:
            with open(self.home_path + "/.config/fast-translate/config.json", "r") as f:
                cfg = json.load(f)
            cfg["baiduSecret"]["appid"] = appid
            cfg["baiduSecret"]["appkey"] = appkey
            with open(self.home_path + "/.config/fast-translate/config.json", "w") as f:
                json.dump(cfg, f)
        except Exception as e:
            logging.error(e.__str__())
            return False
        return True

    @refresh_config
    def change_google_proxy(self, protocol: str, proxy: str):
        try:
            with open(self.home_path + "/.config/fast-translate/config.json", "r") as f:
                cfg = json.load(f)
            cfg["googleSecret"]["proxies"][protocol] = proxy
            with open(self.home_path + "/.config/fast-translate/config.json", "w") as f:
                json.dump(cfg, f)
        except Exception as e:
            logging.error(e.__str__())
            return False
        return True


if __name__ == '__main__':
    config = Configuration()
    print(config.google_proxies)
    config.change_google_proxy("https://", "http://127.0.0.1:7890")
    print(config.google_proxies)
