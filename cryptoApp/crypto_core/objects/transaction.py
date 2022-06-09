from datetime import datetime
import operator as op

from . import CryptoAppObject, Currency, Cryptocurrency
from ..db import CryptoDatabase


class Transaction(CryptoAppObject):
    """Define a transaction between 2 currencies.

    Attributes
    ----------
    currency_send : Currency
        The currency send (spend) by the user.
    amount_send : float
        The amount send (spend) by the user.
    currency_received : Currency
        The currency received (bought) by the user.
    amount_received : float
        The amount received (bought) by the user

    Methods
    -------

    Classmethods
    ------------
    """

    def __init__(self,
                 id_: int,
                 send: tuple[Currency, float],
                 received: tuple[Currency, float],
                 date: datetime = datetime.now()):
        super().__init__(id_)
        self.currency_send = send[0]
        self.amount_send = send[1]
        self.currency_received = received[0]
        self.amount_received = received[1]
        self.date = date

    def __str__(self) -> str:
        """Returns main info on object in a string.

        Returns
        -------
        str : The string format of object.

        """
        return f"<{self.__class__.__name__}(id: {self.id}, send: {self.amount_send}"\
               f"{self.currency_send.ticker.upper()}, received: {self.amount_received}"\
               f"{self.currency_received.ticker.upper()}, date: {self.date})>"

    def __repr__(self) -> str:
        """Return a string representation of transaction.

        Returns
        -------
        str : The string representation.

        """
        return self.__str__()

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

    @staticmethod
    def __crypto_from_db(crypto_data: dict) -> Cryptocurrency:
        """Returns the Cryptocurrency from database in a select transaction."""
        if crypto_data[f'idCurrency'] in Cryptocurrency.CRYPTOCURRENCIES:
            return Cryptocurrency.CRYPTOCURRENCIES[crypto_data[f'idCurrency']]

        if crypto_data[f'idCurrency'] in Currency.CURRENCIES:
            return Currency.CURRENCIES[crypto_data[f'idCurrency']]

        return Cryptocurrency.from_db_dict(crypto_data)



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
                send=(
                    cls.__crypto_from_db({
                        'idCurrency': dico['idCurrencySend'],
                        'name': dico['nameSend'],
                        'ticker': dico['tickerSend'],
                        'price': dico['priceSend'],
                        'circulatingSupply': dico['circulatingSupplySend'],
                        'last_update': dico['lastUpdateSend'],
                        'rank': dico['rankSend']
                    }),
                    dico['amountSend']
                ),
                received=(
                    cls.__crypto_from_db({
                        'idCurrency': dico['idCurrencyReceived'],
                        'name': dico['nameReceived'],
                        'ticker': dico['tickerReceived'],
                        'price': dico['priceReceived'],
                        'circulatingSupply': dico['circulatingSupplyReceived'],
                        'last_update': dico['lastUpdateReceived'],
                        'rank': dico['rankReceived']
                    }),
                    dico['amountReceived']
                ),
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
                result['idTransaction'],
                send=(
                    cls.__crypto_from_db({
                        'idCurrency': result['idCurrencySend'],
                        'name': result['nameSend'],
                        'ticker': result['tickerSend'],
                        'price': result['priceSend'],
                        'circulatingSupply': result['circulatingSupplySend'],
                        'last_update': result['lastUpdateSend'],
                        'rank': result['rankSend']
                    }),
                    result['amountSend']
                ),
                received=(
                    cls.__crypto_from_db({
                        'idCurrency': result['idCurrencyReceived'],
                        'name': result['nameReceived'],
                        'ticker': result['tickerReceived'],
                        'price': result['priceReceived'],
                        'circulatingSupply': result['circulatingSupplyReceived'],
                        'last_update': result['lastUpdateReceived'],
                        'rank': result['rankReceived']
                    }),
                    result['amountReceived']
                ),
                date=result['date']
            )

