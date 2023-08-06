from .IReaderBankStatement import IReaderBankStatement
from ofxReaderBR.model.BankStatement import BankStatement
from ofxReaderBR.model.Origin import Origin

from decimal import Decimal

import logging

logger = logging.getLogger(__name__)


class OFXReaderBankStatement(IReaderBankStatement):

    def __init__(self):
        self.status = 'waiting'

    def read(self, factory, ofx, options=None):
        signal_multiplier = 1
        if options:
            if options['creditcard'] is True and options['bancodobrasil'] is False:
                signal_multiplier = -1

        stmts = ofx.statements

        cs_reader = factory.createReaderCashFlow()

        bank_stmts = []

        self.status = 'complete'
        # btmts -> bs
        for stmt in stmts:
            bs = BankStatement()
            account = stmt.account
            origin = Origin(account)

            txs = stmt.transactions

            for tx in txs:
                cs = cs_reader.read(factory, tx)
                cs.value = Decimal(cs.value)
                cs.value *= signal_multiplier

                cs.origin = origin
                if origin.is_bank_account():
                    cs.cash_date = cs.date
                if options['creditcard'] and options.get('bradesco'):
                    cs.cash_date = stmt.dtstart
                    # TODO: BB
                    # TODO: other banks

                if cs.is_valid():
                    if cs.value >= Decimal(0.0):
                        bs.inflows.append(cs)
                    else:
                        bs.outflows.append(cs)
                else:
                    self.status = 'incomplete'

            bank_stmts.append(bs)

        return bank_stmts
