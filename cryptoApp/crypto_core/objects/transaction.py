from datetime import datetime
import operator as op

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

    def __compare(self, other, operator) -> bool:
        """Compare self to other with the operator specified.

        Parameters
        ----------
        other : Transaction
            A other transaction to compare with self
        operator : function
            operator to use

        Returns
        -------
        bool
            The result of the operation

        Raises
        ------
        ValueError
            Raised if other is not an instance of Transaction
        """
        if not isinstance(other, Transaction):
            raise ValueError(f"Can't compare a Transaction with a '{type(other)}'")
        return operator(self.date, other.date)

    def __eq__(self, o: object) -> bool:
        return self.__compare(o, op.eq)

    def __ne__(self, o: object) -> bool:
        return self.__compare(o, op.ne)

    def __gt__(self, o: object) -> bool:
        return self.__compare(o, op.gt)

    def __ge__(self, o: object) -> bool:
        return self.__compare(o, op.ge)

    def __lt__(self, o: object) -> bool:
        return self.__compare(o, op.lt)

    def __le__(self, o: object) -> bool:
        return self.__compare(o, op.le)

    def delete(self, database: CryptoDatabase, commit: bool = True):
        """Delete the transaction from the database."""
        return database.delete_transactions([self.id], commit=commit)

    @staticmethod
    def multi_delete(transactions: list, database: CryptoDatabase, commit: bool = True):
        """Delete a list of transactions from the database."""
        return database.delete_transactions([t.id for t in transactions], commit=commit)

    @classmethod
    def from_filter(cls, portofolio_id: int, database: CryptoDatabase, /,
                    currency_send: Currency = None,
                    currency_received: Currency = None,
                    **kwargs) -> list:
        """Returns the list of transactions with conditions passed in parameters."""
        if currency_send is not None:
            kwargs['currency_send_id'] = currency_send.id
        if currency_received is not None:
            kwargs['currency_received_id'] = currency_received.id
        return [
            cls(
                dico['idTransaction'],
                send=(dico['currencySend'], dico['amountSend']),
                received=(dico['currencyReceived'], dico['amountReceived']),
                date=dico['date']
            )
            for dico in database.get_transactions_filter(portofolio_id, **kwargs)
        ]

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
