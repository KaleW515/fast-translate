from core.api.server import baidu
from core.api.server import google, google_cn
from core.constants.translator_enums import TranslatorEnums


class Translator:

    def __init__(self):
        import container
        self.config = container.get_container().config
        self.__instance = {
            TranslatorEnums.BAIDU: baidu.BaiduTranslator(secrets=self.config.baidu_secrets),
            TranslatorEnums.GOOGLE: google.GoogleTranslator(secrets=self.config.google_secrets),
            TranslatorEnums.GOOGLECN: google_cn.GoogleCNTranslator()
        }

    async def translate(self, original, translator, target):
        res, success = await self.__instance[translator].translate(original, target=target)
        return res, success
