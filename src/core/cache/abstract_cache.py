from abc import abstractmethod


class AbstractCache:

    @abstractmethod
    def set(self, original: str, result: str, server: str) -> bool:
        pass

    @abstractmethod
    def set_with_ttl(self, original: str, result: str, time: int, server: str) -> bool:
        pass

    @abstractmethod
    def get(self, original: str, server: str) -> str:
        pass
