import asyncio
import random
from typing import List, Union, Dict

import httpx

from core.api.abstract_translator import AbstractTranslator
from core.config.secrets.google_secrets import GoogleSecrets


class TranslateResponse:

    def __init__(self, translated_text: str, detected_source_language: str = None, model: str = None):
        if isinstance(translated_text, list):
            self.translated_text = translated_text[0]
            self.detected_source_language = translated_text[1]
        else:
            self.translated_text = translated_text
            self.detected_source_language = detected_source_language
        self.model = model

    def __repr__(self):
        return self.__class__.__qualname__ + f'(translatedText={repr(self.translated_text)}, detectedSourceLanguage=' \
                                             f'{repr(self.detected_source_language)}, model={repr(self.model)})'


class GoogleTranslator(AbstractTranslator):
    def __init__(
            self,
            target: str = 'zh-CN',
            source: str = 'auto',
            fmt='html',
            user_agent: str = None,
            domain: str = 'com',
            secrets: GoogleSecrets = None
    ):
        self.target = target
        self.source = source
        self.fmt = fmt

        if user_agent is None:
            self.user_agent = (
                f'GoogleTranslate/6.{random.randint(10, 100)}.0.06.{random.randint(111111111, 999999999)}'
                ' (Linux; U; Android {random.randint(5, 11)}; {base64.b64encode(str(random.random())['
                '2:].encode()).decode()}) '
            )
        self.BASE_URL: str = 'https://translate.google.' + domain
        self.LANGUAGE_URL: str = f'{self.BASE_URL}/translate_a/l'
        self.DETECT_URL: str = f'{self.BASE_URL}/translate_a/single'
        self.TRANSLATE_URL: str = f'{self.BASE_URL}/translate_a/t'
        self.TTS_URL: str = f'{self.BASE_URL}/translate_tts'
        self.proxies = secrets.proxies

    async def translate(self, original, target):
        return await self.__do_translate(original, target=target)

    async def __do_translate(
            self, q: Union[str, List[str]], target: str = None, source: str = None, fmt: str = None
    ) -> (str, bool):
        if not q:
            return "没有复制任何内容", True
        if isinstance(q, str):
            if q == '':
                return "没有复制任何内容", True

        for i in range(1, 2):
            response = await self.__do_translate0(q=q, target=target, source=source, fmt=fmt, v='1.0')
            if response is None:
                return "网络异常，请检查代理", False
            if response.status_code == 429:
                continue
            break
        # noinspection PyUnboundLocalVariable
        if response is None:
            return "网络异常, 请检查代理", False
        # noinspection PyUnboundLocalVariable
        if response.status_code == 200:
            ll = [TranslateResponse(translated_text=i) for i in response.json()]
            return ll[0].translated_text, True
        return response.text, False

    async def __do_translate0(
            self, q: Union[str, List[str]], target: str = None, source: str = None, fmt: str = None, v: str = None
    ):
        if target is None:
            target = self.target
        if source is None:
            source = self.source
        if fmt is None:
            fmt = self.fmt
        for i in range(1, 4):
            if self.proxies is None:
                try:
                    async with httpx.AsyncClient(trust_env=False, timeout=2) as httpxClient:
                        response = await httpxClient.post(
                            self.TRANSLATE_URL,
                            params={'tl': target, 'sl': source, 'ie': 'UTF-8', 'oe': 'UTF-8', 'client': 'at', 'dj': '1',
                                    'format': fmt, 'v': v},
                            data={'q': q}
                        )
                        if response.status_code == 429:
                            continue
                        break
                except Exception as e:
                    return None
            else:
                try:
                    async with httpx.AsyncClient(proxies=self.proxies, timeout=2) as httpxClient:
                        response = await httpxClient.post(
                            self.TRANSLATE_URL,
                            params={'tl': target, 'sl': source, 'ie': 'UTF-8', 'oe': 'UTF-8', 'client': 'at', 'dj': '1',
                                    'format': fmt, 'v': v},
                            data={'q': q}
                        )
                        if response.status_code == 429:
                            continue
                        break
                except Exception as e:
                    return None
        # noinspection PyUnboundLocalVariable
        return response


if __name__ == '__main__':
    client = GoogleTranslator(proxies={'https://': 'http://localhost:7890'})
    # client = GoogleTranslator()
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(client.translate('hello', target='zh'))
    loop.run_until_complete(future)
    print(future.result())
