import abc

from ofxReaderBR.model.BankStatement import BankStatement

class IReaderBankStatement(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def read(self, factory, ofx, options) -> BankStatement:
        pass