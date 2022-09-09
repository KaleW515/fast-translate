from api.server import baidu, google, google_cn


class Translator:

    def __init__(self):
        import container
        self.config = container.get_container().config
        self.__instance = {
            "baidu": baidu.BaiduTranslator(),
            "googlecn": google_cn.GoogleCNTranslator(),
            "google": google.GoogleTranslator(proxies=self.config.google_proxies)
        }

    async def translate(self, original, translator: str, target):
        res, success = await self.__instance[translator].translate(original, target=target)
        return res, success
