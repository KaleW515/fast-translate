import hashlib
import json
import random
import urllib

import httpx

from core.translate.abstract_translator import AbstractTranslator
from core.config.secrets.baidu_secrets import BaiduSecrets


class BaiduTranslator(AbstractTranslator):
    def __init__(self, secrets: BaiduSecrets):
        import container
        self.config = container.get_container().config
        self.url = "https://fanyi-api.baidu.com/api/trans/vip/translate?q={}&from={}&to={" \
                   "}&appid={}&salt={}&sign={}"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/102.0.5005.61 Safari/537.36"
        }
        self.app_id = secrets.app_id
        self.app_key = secrets.app_key

    def __get_sign_salt(self, original):
        salt = random.randint(32768, 65536)
        sign = self.app_id + original + str(salt) + self.app_key
        sign = hashlib.md5(sign.encode()).hexdigest()
        return sign, salt

    async def translate(self, original, target):
        return await self.__do_translate(original, target=target)

    async def __do_translate(self, original, text_from="auto", target="zh") -> (str, bool):
        if self.app_id == "" or self.app_key == "" or self.app_id is None or self.app_key is None:
            return "百度翻译接口未配置", False
        sign, salt = self.__get_sign_salt(original)
        url = self.url.format(urllib.parse.quote(original), text_from, target, self.app_id, salt,
                              sign)
        async with httpx.AsyncClient() as client:
            res = await client.get(url=url, headers=self.headers)
            res = json.loads(res.text)
            if 'trans_result' in res:
                try:
                    return res['trans_result'][0]['dst'], True
                except:
                    return "", False
            elif "error_msg" in res:
                return res["error_msg"], False
