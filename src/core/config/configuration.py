import json
import logging
import os
import shutil

from core.config.secrets import baidu_secrets, google_secrets, redis_secrets
from core.constants.copykey_map import CopykeyMap, CopykeyEnums
from core.constants.file_constants import FileConstants
from core.constants.target_constants import Constants
from core.utils import log

logging.basicConfig(level=log.get_log_config()[0], filename=log.get_log_config()[1],
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


class Configuration:

    def __init__(self):
        self.baidu_secret_name = "baiduSecret"
        self.google_secret_name = "googleSecret"
        self.redis_secret_name = "redisSecret"
        self.target_list = None
        self.baidu_target = None
        self.google_target = None
        self.googlecn_target = None

        self.baidu_secrets = None
        self.google_secrets = None

        self.redis_secrets = None

        self.__check_config()
        self.__check_config_complete()
        self.__check_log()
        self.__constant_init()
        self.__secret_init()

    def __constant_init(self):
        self.target_list = Constants.TARGET_LIST
        self.baidu_target = Constants.BAIDU_TARGET
        self.google_target = Constants.GOOGLE_TARGET
        self.googlecn_target = Constants.GOOGLE_CN_TARGET
        logging.info("init constant success ~")
        return

    def __secret_init(self):
        try:
            with open(FileConstants.CONFIG_FILE_PATH, "r") as f:
                cfg = json.load(f)
                self.__do_baidu_secret_init(cfg)

                self.__do_google_secret_init(cfg)

                self.__do_redis_secret_init(cfg)
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

    def __do_redis_secret_init(self, cfg: dict):
        self.redis_secrets = redis_secrets.RedisSecrets()
        if cfg[self.redis_secret_name]["host"] != "":
            self.redis_secrets.host = cfg[self.redis_secret_name]["host"]
        if cfg[self.redis_secret_name]["port"] != "":
            self.redis_secrets.port = cfg[self.redis_secret_name]["port"]
        if cfg[self.redis_secret_name]["password"] != "":
            self.redis_secrets.password = cfg[self.redis_secret_name]["password"]

    def __check_config(self):
        os.makedirs(FileConstants.CONFIG_DIR_PATH, exist_ok=True)
        if not os.path.exists(FileConstants.CONFIG_FILE_PATH):
            # 将config_template.json复制到config.json
            shutil.copy(FileConstants.CONFIG_TEMPLATE_FILE_PATH, FileConstants.CONFIG_FILE_PATH)
        logging.info("check config finish ~")

    def __check_config_complete(self):
        try:
            with open(FileConstants.CONFIG_FILE_PATH, "r") as f:
                cfg = json.load(f)
                if self.baidu_secret_name not in cfg.keys():
                    cfg[self.baidu_secret_name] = {}
                    cfg[self.baidu_secret_name]["appid"] = ""
                    cfg[self.baidu_secret_name]["appKey"] = ""
                if self.google_secret_name not in cfg.keys():
                    cfg[self.google_secret_name] = {}
                    cfg[self.google_secret_name]["proxies"] = {}
                if self.redis_secret_name not in cfg.keys():
                    cfg[self.redis_secret_name] = {}
                    cfg[self.redis_secret_name]["host"] = ""
                    cfg[self.redis_secret_name]["port"] = ""
                    cfg[self.redis_secret_name]["password"] = ""
            with open(FileConstants.CONFIG_FILE_PATH, "w") as f:
                json.dump(cfg, f)
        except Exception as e:
            logging.error(e.__str__())
            return False

    def refresh_config(self):
        self.__check_config()
        self.__constant_init()
        self.__secret_init()

    def change_baidu_secret(self, appid: str, appkey: str):
        try:
            with open(FileConstants.CONFIG_FILE_PATH, "r") as f:
                cfg = json.load(f)
            cfg[self.baidu_secret_name]["appid"] = appid
            cfg[self.baidu_secret_name]["appKey"] = appkey
            with open(FileConstants.CONFIG_FILE_PATH, "w") as f:
                json.dump(cfg, f)
            self.refresh_config()
        except Exception as e:
            logging.error(e.__str__())
            return False
        return True

    def change_google_proxy(self, protocol: str, proxy: str):
        try:
            with open(FileConstants.CONFIG_FILE_PATH, "r") as f:
                cfg = json.load(f)
            cfg[self.google_secret_name]["proxies"] = {
                protocol: proxy
            }
            with open(FileConstants.CONFIG_FILE_PATH, "w") as f:
                json.dump(cfg, f)
            self.refresh_config()
        except Exception as e:
            logging.error(e.__str__())
            return False
        return True

    def change_redis_secret(self, host: str, port: int, password: str):
        try:
            with open(FileConstants.CONFIG_FILE_PATH, "r") as f:
                cfg = json.load(f)
            cfg[self.redis_secret_name]["host"] = host
            cfg[self.redis_secret_name]["port"] = port
            cfg[self.redis_secret_name]["password"] = password
            with open(FileConstants.CONFIG_FILE_PATH, "w") as f:
                json.dump(cfg, f)
            self.refresh_config()
        except Exception as e:
            logging.error(e.__str__())
            return False
        return True

    def get_google_secret(self) -> google_secrets.GoogleSecrets:
        return self.google_secrets

    def get_baidu_secret(self) -> baidu_secrets.BaiduSecrets:
        return self.baidu_secrets

    def get_redis_secret(self) -> redis_secrets.RedisSecrets:
        return self.redis_secrets

    def get_copykey(self) -> list:
        copykey = []
        try:
            with open(FileConstants.COPYKEY_FILE_PATH, "r") as f:
                while f.readable():
                    key = f.readline().replace("\n", "")
                    if key == "":
                        break
                    copykey.append(CopykeyMap.copykey_map[key])
        except FileNotFoundError as e:
            copykey.append(CopykeyMap.copykey_map[CopykeyEnums.CTRL.value])
            copykey.append(CopykeyMap.copykey_map[CopykeyEnums.C.value])
        return copykey

    def save_copykey(self, copykey: list) -> bool:
        try:
            with open(FileConstants.COPYKEY_FILE_PATH, "w") as f:
                for i in range(len(copykey)):
                    f.write(str(copykey[i]) + "\n")
            return True
        except:
            return False

    def __check_log(self):
        os.makedirs(FileConstants.LOG_DIR_PATH, exist_ok=True)
        logging.info("check log path finish ~")


if __name__ == '__main__':
    config = Configuration()
    print(config.google_secrets.proxies)
    config.change_google_proxy("https://", "http://127.0.0.1:7890")
    print(config.google_secrets.proxies)
