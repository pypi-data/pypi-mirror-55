from ..IReaderCashFlow import IReaderCashFlow
from ofxReaderBR.model.CashFlow import CashFlow, CashFlowType
from ofxReaderBR.model.Origin import Origin, AccountType

from collections import namedtuple

import logging

logger = logging.getLogger(__name__)

class XLSReaderCashFlow(IReaderCashFlow):
    def read(self, factory, ofx) -> CashFlow:
        cs = CashFlow()

        row = ofx
        
        cellValues = []
        for cellValue in row:
            cellValues.append(cellValue)

        Account = namedtuple('Account', 'acctid')
        account = Account(acctid = cellValues[1])
        origin = Origin(account)

        if cellValues[0].upper() == 'C/C':
            origin.account_type = AccountType.BANKACCOUNT
        else:
            origin.account_type = AccountType.CREDITCARD

        cs.origin = origin
        cs.date = cellValues[2]
        cs.cash_date = cellValues[3]
        cs.name = cellValues[4]
        cs.value = cellValues[5]

        return cs
