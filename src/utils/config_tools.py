import json
import os
import shutil

path = {
    "home_path": os.getenv("HOME"),
}


def get_config_constant():
    with open("./config/constants.json", "r") as f:
        cfg = json.load(f)
    return cfg


def get_config_secret():
    check_config()
    with open(path["home_path"] + "/.config/fast-translate/config.json", "r") as f:
        cfg = json.load(f)
    return cfg


def check_config():
    if not os.path.exists(path["home_path"] + "/.config"):
        os.mkdir(path["home_path"] + "/.config")
    if not os.path.exists(path["home_path"] + "/.config/fast-translate"):
        os.mkdir(path["home_path"] + "/.config/fast-translate")
    if not os.path.exists(path["home_path"] + "/.config/fast-translate/config.json"):
        # 将config_template.json复制到config.json
        shutil.copy("./config/config_template.json", path["home_path"] + "/.config/fast-translate/config.json")


def change_baidu_secret(appid: str, appkey: str):
    try:
        with open(path["home_path"] + "/.config/fast-translate/config.json", "r") as f:
            cfg = json.load(f)
        cfg["baiduSecret"]["appid"] = appid
        cfg["baiduSecret"]["appkey"] = appkey
        with open(path["home_path"] + "/.config/fast-translate/config.json", "w") as f:
            json.dump(cfg, f)
    except Exception as e:
        return False
    return True


def change_google_proxy(protocol: str, proxy: str):
    try:
        with open(path["home_path"] + "/.config/fast-translate/config.json", "r") as f:
            cfg = json.load(f)
        cfg["googleSecret"]["proxies"][protocol] = proxy
        with open(path["home_path"] + "/.config/fast-translate/config.json", "w") as f:
            json.dump(cfg, f)
    except Exception as e:
        return False
    return True


if __name__ == '__main__':
    check_config()
