from core.cache.impl.dict_cache import DictCache
from core.cache.impl.redis_cache import RedisCache


class CacheCenter:
    def __init__(self):
        import container
        self.cfg = container.get_container().config
        self.redis_secret = self.cfg.redis_secrets
        if self.redis_secret.password is None or self.redis_secret.password == "":
            self.rd = RedisCache(host=self.redis_secret.host, port=self.redis_secret.port)
        else:
            self.rd = RedisCache(host=self.redis_secret.host, port=self.redis_secret.port,
                                 password=self.redis_secret.password)
        self.dict_cache = DictCache()

    def get_cache(self, original: str, server: str) -> str:
        redis_res = self.rd.get(original, server)
        if redis_res != "":
            return redis_res
        else:
            return self.dict_cache.get(original, server)

    def set_cache(self, original: str, result: str, server: str):
        if self.rd.set(original, result, server):
            return
        else:
            self.dict_cache.set(original, result, server)
