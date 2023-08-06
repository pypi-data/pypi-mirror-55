import abc
from typing import List

from ofxReaderBR.model.BankStatement import BankStatement

class IReaderController(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def read(self, factory, files=[]) -> List[BankStatement]:
        pass