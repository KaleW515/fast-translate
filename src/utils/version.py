import json

import requests

VERSION = "1.0.0"


def check_update():
    url = "https://gitee.com/api/v5/repos/kalew515/fast-translate/releases/latest"
    res = json.loads(requests.get(url=url).text)
    return res["tag_name"] != VERSION
