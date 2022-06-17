from api.server import baidu, google
from utils import config_tools


class Translator:

    def __init__(self):
        self.__instance = {
            "baidu": baidu.BaiduTranslator(),
        }
        if config_tools.get_config_secret()["googleSecret"]["proxies"] != "":
            self.__instance["google"] = google.GoogleTranslator(
                proxies=config_tools.get_config_secret()["googleSecret"]["proxies"])

    async def translate(self, original, translator: str, target):
        res, success = await self.__instance[translator].translate(original, target=target)
        return res, success
