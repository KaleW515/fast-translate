from abc import abstractmethod


class AbstractTranslator:

    @abstractmethod
    def translate(self, original, target):
        pass
