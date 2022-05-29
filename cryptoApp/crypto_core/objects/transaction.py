from datetime import datetime

from . import Currency
from crypto_common.db import CryptoDatabase


class Transaction:
    """Define a transaction between 2 currencies.
    """

    def __init__(self,
                 id_: int,
                 send: tuple[Currency, float],
                 received: tuple[Currency, float],
                 date: datetime = datetime.now()):
        self.id = id_
        self.currency_send = send[0]
        self.amount_send = send[1]
        self.currency_received = received[0]
        self.currency_received = received[1]
        self.date = date

    @classmethod
    def from_id(cls, id_: int, database: CryptoDatabase):
        result = database.get_transaction_by_id(id_)
        if result is not None:
            return cls(
                id_,
                send=(result['currencySend'], result['amountSend']),
                received=(result['currencyReceived'], result['amountReceived']),
                date=result['date']
            )
