from .ReaderAbstractFactory import ReaderAbstractFactory

from ofxReaderBR.reader.IReaderCashFlow import IReaderCashFlow
from ofxReaderBR.reader.IReaderBankStatement import IReaderBankStatement
from ofxReaderBR.reader.IReaderController import IReaderController

from ofxReaderBR.reader.xml.XMLReaderCashFlow import XMLReaderCashFlow
from ofxReaderBR.reader.xml.XMLReaderBankStatement import XMLReaderBankStatement
from ofxReaderBR.reader.xml.XMLReaderController import XMLReaderController

class XMLReaderFactory(ReaderAbstractFactory):
    def createReaderController(self) -> IReaderController:
        return XMLReaderController()

    def createReaderBankStatement(self) -> IReaderBankStatement:
        return XMLReaderBankStatement()
    
    def createReaderCashFlow(self) -> IReaderCashFlow:
        return XMLReaderCashFlow()