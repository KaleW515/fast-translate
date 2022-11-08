import time as tm

import core.utils.hash as hash_util
from core.cache.abstract_cache import AbstractCache


class DictEntry:

    def __init__(self, result: str, ttl: int):
        self.result = result
        self.ttl = ttl


class DictCache(AbstractCache):

    def __init__(self):
        self.cache = dict()

    def set(self, original: str, result: str, server: str) -> bool:
        return self.set_with_ttl(original, result, 60 * 60 * 24, server)

    def set_with_ttl(self, original: str, result: str, time: int, server: str) -> bool:
        try:
            key = hash_util.get_hash(original + server)
            self.cache[key] = DictEntry(result, int(tm.time()) + time)
            return True
        except:
            return False

    def get(self, original: str, server: str) -> str:
        self.detect_ttl()
        key = hash_util.get_hash(original + server)
        if key in self.cache.keys() and self.cache[key].ttl < int(tm.time()):
            return self.cache[key]
        else:
            return ""

    def detect_ttl(self):
        keys = self.cache.keys()
        length = len(keys) / 10
        count = 0
        for key in keys:
            if count >= length:
                break
            count += 1
            if self.cache[key].ttl < int(tm.time()):
                self.cache.pop(key)
