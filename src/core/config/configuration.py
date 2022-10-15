import json
import logging
import os
import shutil

from core.config.constants import Constants
from core.config.secrets import baidu_secrets, google_secrets
from core.utils import log

logging.basicConfig(level=log.get_log_config()[0], filename=log.get_log_config()[1],
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


class Configuration:

    def __init__(self):
        self.home_path = os.getenv("HOME")
        # config 文件路径
        self.config_dir_path = self.home_path + "/.config/fast-translate"
        # config 模板文件路径
        self.config_template_file_path = "../../data/config_template.json"
        # config 文件全路径
        self.config_file_path = self.config_dir_path + "/config.json"
        self.baidu_secret_name = "baiduSecret"
        self.google_secret_name = "googleSecret"
        self.target_list = None
        self.baidu_target = None
        self.google_target = None
        self.googlecn_target = None

        self.baidu_secrets = None
        self.google_secrets = None

        self.check_config()
        self.constant_init()
        self.secret_init()

    def constant_init(self):
        self.target_list = Constants.TARGET_LIST
        self.baidu_target = Constants.BAIDU_TARGET
        self.google_target = Constants.GOOGLE_TARGET
        self.googlecn_target = Constants.GOOGLE_CN_TARGET
        logging.info("init constant success ~")
        return

    def secret_init(self):
        try:
            with open(self.config_file_path, "r") as f:
                cfg = json.load(f)
                self.__do_baidu_secret_init(cfg)

                self.__do_google_secret_init(cfg)
            logging.info("init secret success ~")
        except:
            raise IOError("parse config.json failed, please check again ~")
        return

    def __do_baidu_secret_init(self, cfg: dict):
        self.baidu_secrets = baidu_secrets.BaiduSecrets()
        if cfg[self.baidu_secret_name]["appid"] != "":
            self.baidu_secrets.app_id = cfg[self.baidu_secret_name]["appid"]
        if cfg[self.baidu_secret_name]["appKey"] != "":
            self.baidu_secrets.app_key = cfg[self.baidu_secret_name]["appKey"]

    def __do_google_secret_init(self, cfg: dict):
        self.google_secrets = google_secrets.GoogleSecrets()
        if cfg[self.google_secret_name]["proxies"] != "":
            self.google_secrets.proxies = cfg[self.google_secret_name]["proxies"]

    def check_config(self):
        os.makedirs(self.config_dir_path, exist_ok=True)
        if not os.path.exists(self.config_file_path):
            # 将config_template.json复制到config.json
            shutil.copy(self.config_template_file_path, self.config_file_path)
        logging.info("check config finish ~")

    @staticmethod
    def refresh_config(func):
        def wrap(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self.check_config()
            self.constant_init()
            self.secret_init()

        return wrap

    @refresh_config
    def change_baidu_secret(self, appid: str, appkey: str):
        try:
            with open(self.config_file_path, "r") as f:
                cfg = json.load(f)
            cfg[self.baidu_secret_name]["appid"] = appid
            cfg[self.baidu_secret_name]["appkey"] = appkey
            with open(self.config_file_path, "w") as f:
                json.dump(cfg, f)
        except Exception as e:
            logging.error(e.__str__())
            return False
        return True

    @refresh_config
    def change_google_proxy(self, protocol: str, proxy: str):
        try:
            with open(self.config_file_path, "r") as f:
                cfg = json.load(f)
            cfg[self.google_secret_name]["proxies"][protocol] = proxy
            with open(self.config_file_path, "w") as f:
                json.dump(cfg, f)
        except Exception as e:
            logging.error(e.__str__())
            return False
        return True


if __name__ == '__main__':
    config = Configuration()
    print(config.google_secret.proxies)
    config.change_google_proxy("https://", "http://127.0.0.1:7890")
    print(config.google_secret.proxies)
