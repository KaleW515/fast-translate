from api.server import baidu, google, google_cn
from utils import config_tools


class Translator:

    def __init__(self):
        self.__instance = {
            "baidu": baidu.BaiduTranslator(),
            "googlecn": google_cn.GoogleCNTranslator()
        }
        if config_tools.get_config_secret()["googleSecret"]["proxies"] != "":
            self.__instance["google"] = google.GoogleTranslator(
                proxies=config_tools.get_config_secret()["googleSecret"]["proxies"])
        else:
            self.__instance["google"] = google.GoogleTranslator()

    async def translate(self, original, translator: str, target):
        res, success = await self.__instance[translator].translate(original, target=target)
        return res, success
