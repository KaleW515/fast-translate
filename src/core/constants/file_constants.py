import os


class FileConstants:
    # home 路径
    HOME_PATH = os.getenv("HOME")

    # config 文件路径
    CONFIG_DIR_PATH = HOME_PATH + "/.config/fast-translate"

    # log 文件路径
    LOG_DIR_PATH = HOME_PATH + "/.cache/fast-translate"

    # config 模板文件路径
    CONFIG_TEMPLATE_FILE_PATH = "/opt/fast-translate/data/config_template.json"

    # config 文件全路径
    CONFIG_FILE_PATH = CONFIG_DIR_PATH + "/config.json"

    # log 文件全路径
    LOG_FILE_PATH = LOG_DIR_PATH + "/ft.log"

    # 复制快捷键文件路径
    COPYKEY_FILE_PATH = CONFIG_DIR_PATH + "/copykey.conf"

    # logo路径
    LOGO_FILE_PATH = "data/icon/logo.svg.png"
