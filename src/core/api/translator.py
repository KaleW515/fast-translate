from core.api.server import baidu
from core.api.server import google, google_cn
from core.config.translator_enums import TranslatorEnums


class Translator:

    def __init__(self):
        import container
        self.config = container.get_container().config
        self.__instance = {
            TranslatorEnums.BAIDU.value: baidu.BaiduTranslator(self.config.baidu_app_id, self.config.baidu_app_key),
            TranslatorEnums.GOOGLE.value: google_cn.GoogleCNTranslator(),
            TranslatorEnums.GOOGLECN.value: google.GoogleTranslator(proxies=self.config.google_proxies)
        }

    async def translate(self, original, translator, target):
        res, success = await self.__instance[translator].translate(original, target=target)
        return res, success
