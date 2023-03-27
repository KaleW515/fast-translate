import json

import requests

from core.constants.links import Links

VERSION = "1.2.2"


def check_update():
    url = Links.CHECK_UPDATE_URL
    res = json.loads(requests.get(url=url).text)
    return res["tag_name"] != VERSION
