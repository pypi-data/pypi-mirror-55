import logging
from decimal import Decimal

from ofxReaderBR.model.BankStatement import BankStatement
from ..IReaderBankStatement import IReaderBankStatement

logger = logging.getLogger(__name__)


class XLSReaderBankStatement(IReaderBankStatement):

    def __init__(self):
        self.status = 'waiting'

    def read(self, factory, ofx, options=None) -> BankStatement:
        bs = BankStatement()

        ws = ofx

        cs_reader = factory.createReaderCashFlow()
        header_row = True
        self.status = 'complete'
        for row in ws.values:
            # Pulando o cabeçalho
            if header_row:
                header_row = False
                continue

            cs = cs_reader.read(factory, row)
            if cs.is_valid():
                if isinstance(cs.value, str):
                    cs.value = Decimal(cs.value.replace(',', '.'))
                if cs.value >= Decimal(0.0):
                    bs.inflows.append(cs)
                else:
                    bs.outflows.append(cs)
            else:
                self.status = 'incomplete'

        return bs
