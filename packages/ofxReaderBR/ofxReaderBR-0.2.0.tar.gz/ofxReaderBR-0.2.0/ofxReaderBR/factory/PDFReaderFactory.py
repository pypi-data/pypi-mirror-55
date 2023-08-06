from .ReaderAbstractFactory import ReaderAbstractFactory

from ofxReaderBR.reader.IReaderCashFlow import IReaderCashFlow
from ofxReaderBR.reader.IReaderBankStatement import IReaderBankStatement

from ofxReaderBR.reader.readercontroller import PDFReaderController, IReaderController
from ofxReaderBR.reader.pdf.PDFReaderCashFlow import PDFReaderCashFlow
from ofxReaderBR.reader.pdf.PDFReaderBankStatement import PDFReaderBankStatement

class PDFReaderFactory(ReaderAbstractFactory):
    def createReaderController(self) -> IReaderController:
        return PDFReaderController()

    def createReaderBankStatement(self) -> IReaderBankStatement:
        return PDFReaderBankStatement()
    
    def createReaderCashFlow(self) -> IReaderCashFlow:
        return PDFReaderCashFlow()