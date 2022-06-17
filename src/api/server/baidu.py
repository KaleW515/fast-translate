import hashlib
import json
import random
import urllib

import httpx

from utils import config_tools


class BaiduTranslator:
    def __init__(self):
        self.url = "https://fanyi-api.baidu.com/api/trans/vip/translate?q={}&from={}&to={}&appid={}&salt={}&sign={}"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/102.0.5005.61 Safari/537.36"
        }
        self.app_id, self.app_key = self.__get_secret()

    def __get_sign_salt(self, original):
        salt = random.randint(32768, 65536)
        sign = self.app_id + original + str(salt) + self.app_key
        sign = hashlib.md5(sign.encode()).hexdigest()
        return sign, salt

    def __get_secret(self):
        cfg = config_tools.get_config_secret()
        return cfg["baiduSecret"]["appid"], cfg["baiduSecret"]["appKey"]

    async def translate(self, original, text_from="auto", target="zh") -> (str, bool):
        if self.app_id == "" or self.app_key == "":
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
            else:
                return "", False
