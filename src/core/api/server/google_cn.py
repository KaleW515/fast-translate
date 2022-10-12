import asyncio
import json

import httpx


class GoogleCNTranslator:
    def __init__(self):
        self.cli = "gtx"
        self.dt = "t"
        self.url = "https://translate.googleapis.com/translate_a/single?client={}&dt={}&sl={}&tl={}&q={}"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/102.0.5005.61 Safari/537.36"
        }

    async def translate(self, original, text_from="auto", target="zh") -> (str, bool):
        url = self.url.format(self.cli, self.dt, text_from, target, original)
        async with httpx.AsyncClient() as client:
            res = await client.post(url=url, headers=self.headers)
            res = json.loads(res.text)
            try:
                ts = ""
                for r in res[0]:
                    ts += r[0]
                return ts, True
            except:
                return "", False


if __name__ == '__main__':
    client = GoogleCNTranslator()
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(client.translate('hello', target='zh'))
    loop.run_until_complete(future)
    print(future.result())
