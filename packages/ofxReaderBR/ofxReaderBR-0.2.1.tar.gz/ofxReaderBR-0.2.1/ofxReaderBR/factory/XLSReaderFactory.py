from .ReaderAbstractFactory import ReaderAbstractFactory

from ofxReaderBR.reader.IReaderCashFlow import IReaderCashFlow
from ofxReaderBR.reader.IReaderBankStatement import IReaderBankStatement

from ofxReaderBR.reader.readercontroller import XLSReaderController, IReaderController
from ofxReaderBR.reader.xls.XLSReaderBankStatement import XLSReaderBankStatement
from ofxReaderBR.reader.xls.XLSReaderCashFlow import XLSReaderCashFlow

class XLSReaderFactory(ReaderAbstractFactory):
    def createReaderController(self) -> IReaderController:
        return XLSReaderController()

    def createReaderBankStatement(self) -> IReaderBankStatement:
        return XLSReaderBankStatement()
    
    def createReaderCashFlow(self) -> IReaderCashFlow:
        return XLSReaderCashFlow()