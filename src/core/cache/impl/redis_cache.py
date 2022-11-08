import pickle

import redis

import core.utils.hash as hash_util
from core.cache.abstract_cache import AbstractCache


class ResultEntry:

    def __init__(self, server: str, result: str):
        self.server = server
        self.result = result


class RedisCache(AbstractCache):

    def __init__(self, host="localhost", port=6379, password=None):
        self.__host = host
        self.__port = port
        self.__password = password
        if self.__password is None:
            self.__poll = redis.ConnectionPool(host=self.__host, port=self.__port,
                                               decode_responses=True)
        else:
            self.__poll = redis.ConnectionPool(host=self.__host, port=self.__port,
                                               decode_responses=True,
                                               password=self.__password)

    def set(self, original: str, result: str, server: str) -> bool:
        return self.set_with_ttl(original, result, 60 * 60 * 24, server)

    def set_with_ttl(self, original: str, result: str, time: int, server: str) -> bool:
        try:
            key = hash_util.get_hash(original + server)
            r = redis.Redis(connection_pool=self.__poll)
            r.set(key, pickle.dumps(ResultEntry(server, result)), ex=time)
            return True
        except:
            return False

    def get(self, original: str, server: str) -> str:
        try:
            key = hash_util.get_hash(original + server)
            r = redis.Redis()
            res = pickle.loads(r.get(key))
            return res.result
        except:
            return ""
