from datetime import datetime

from . import Currency
from ..db import CryptoDatabase


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
    def from_filter(cls, portofolio_id: int, database: CryptoDatabase,
                    currency_send: Currency,
                    currency_received: Currency,
                    **kwargs) -> list:
        kwargs['currency_send_id'] = currency_send.id
        kwargs['currency_received_id'] = currency_received.id
        return database.get_transactions_filter(portofolio_id, **kwargs)

    @classmethod
    def new_transaction(cls,
                        send: tuple[Currency, float],
                        received: tuple[Currency, float],
                        date: datetime,
                        portofolio_id: int,
                        database: CryptoDatabase):
        id_ = database.insert_transaction({
            'date': date,
            'amount_send': send[1],
            'amount_received': received[1],
            'currency_send_id': send[0].id,
            'currency_received_id': received[0].id,
            'portofolio_id': portofolio_id
        })
        return cls(
            id_,
            send,
            received,
            date,
        )

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
