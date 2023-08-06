from .ReaderAbstractFactory import ReaderAbstractFactory

from ofxReaderBR.reader.IReaderCashFlow import IReaderCashFlow
from ofxReaderBR.reader.OFXReaderCashFlow import OFXReaderCashFlow

from ofxReaderBR.reader.IReaderBankStatement import IReaderBankStatement
from ofxReaderBR.reader.OFXReaderBankStatement import OFXReaderBankStatement

from ofxReaderBR.reader.readercontroller import IReaderController
from ofxReaderBR.reader.OFXReaderController import OFXReaderController

class OFXReaderFactory(ReaderAbstractFactory):
    def createReaderController(self) -> IReaderController:
        return OFXReaderController()

    def createReaderBankStatement(self) -> IReaderBankStatement:
        return OFXReaderBankStatement()
    
    def createReaderCashFlow(self) -> IReaderCashFlow:
        return OFXReaderCashFlow()