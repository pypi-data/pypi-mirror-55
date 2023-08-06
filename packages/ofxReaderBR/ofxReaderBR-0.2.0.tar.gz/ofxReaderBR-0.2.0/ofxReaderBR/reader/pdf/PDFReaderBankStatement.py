from ..IReaderBankStatement import IReaderBankStatement
from ofxReaderBR.model.BankStatement import BankStatement

import logging

logger = logging.getLogger(__name__)


class PDFReaderBankStatement(IReaderBankStatement):

    def __init__(self):
        self.status = 'waiting'

    def read(self, factory, ofx, options=None) -> BankStatement:
        bs = BankStatement()

        result = ofx

        csReader = factory.createReaderCashFlow()
        headerRow = True
        self.status = 'complete'
        for row in result:
            # Pulando o cabecalho
            has_header = options.get('has_header', True)
            if headerRow and has_header:
                headerRow = False
                continue

            cs = csReader.read(factory, row)
            if not cs.is_valid():
                self.status = 'incomplete'
            elif '-' not in cs.value:
                bs.inflows.append(cs)
            else:
                bs.outflows.append(cs)

        return bs
