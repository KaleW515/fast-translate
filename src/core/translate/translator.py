from core.constants.translator_enums import TranslatorEnums
from core.translate.server import baidu
from core.translate.server import google, google_cn
from core.cache.cache_center import CacheCenter


class Translator:

    def __init__(self):
        import container
        self.config = container.get_container().config
        self.cache_center = CacheCenter()
        self.__instance = {
            TranslatorEnums.BAIDU: baidu.BaiduTranslator(secrets=self.config.baidu_secrets),
            TranslatorEnums.GOOGLE: google.GoogleTranslator(secrets=self.config.google_secrets),
            TranslatorEnums.GOOGLECN: google_cn.GoogleCNTranslator()
        }

    async def translate(self, original, translator, target, use_cache: bool):
        if use_cache:
            cache = self.cache_center.get_cache(original, translator.value)
            if cache != "":
                return cache, True
        res, success = await self.__instance[translator].translate(original, target=target)
        if success:
            self.cache_center.set_cache(original, res, translator.value)
        return res, success
