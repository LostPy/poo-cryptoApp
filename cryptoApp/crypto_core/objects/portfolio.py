from datetime import datetime

from . import Currency, Cryptocurrency, Transaction
from . import NameableObject
from ..db import CryptoDatabase


class Portfolio(NameableObject):
    """Define a portfolio of an user with the list of transactions.

    Attributes
    ----------
    password : str
        The password for this portfolio (hashed)
    currencies : dict[Currency, float]
        A dictionary with the amount of currency for this portfolio.
    """

    def __init__(self, id_: int, name: str, password: str):
        super().__init__(id_, name)
        self.password = password
        self.currencies = dict()

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password: str):
        if not isinstance(password, str):
            raise ValueError("password must be a str")
        self._password = password

    @property
    def cryptocurrencies(self):
        """Returns `self.currencies` without currencies which are not crypto.
        """
        return {
            c: amount
            for c, amount in self.currencies.items()
            if isinstance(c, Cryptocurrency)
        }

    def __getitem__(self, currency: Cryptocurrency) -> float:
        if not isinstance(currency, Cryptocurrency):
            raise ValueError("The key must be an instance of Cryptocurrency")
        return self.currencies[currency]

    def __setitem__(self, currency: Cryptocurrency, amount: float):
        if not isinstance(currency, Cryptocurrency):
            raise ValueError("The key must be an instance of Cryptocurrency")
        self.currencies[currency] = amount

    def __delitem__(self, currency: Cryptocurrency):
        if not isinstance(currency, Cryptocurrency):
            raise ValueError("The key must be an instance of Cryptocurrency")
        del self.currencies[currency]

    def get(self, currency: Currency) -> float:
        """Returns `self.currencies.get(currency)`.

        Parameters
        ----------
        currency : Currency
            The currency to get the amount."""
        if not isinstance(currency, Currency):
            raise ValueError("The key must be an instance of Currency")
        return self.currencies.get(currency)

    def get_transactions(self,
                         database: CryptoDatabase,
                         start: datetime = None,
                         end: datetime = None) -> list[Transaction]:
        """Get transaction between two dates.

        Parameters
        ----------
        database : CryptoDatabase
           The database connection 
        start : datetime.datetime, optional
            The early datetime, if None, there is not limit.
        end : datetime.datetime, optional
           The lastest datetime, if None, there is not limite.

        Returns
        -------
        list[Transaction] : Transactions between specified dates
        """
        if start is None and end is None:
            range_date = None
        else:
            range_date = (start, end)
        return Transaction.from_filter(self.id, database, range_date=range_date)

    def get_transactions_filtered(self,
                                  database: CryptoDatabase,
                                  **kwargs) -> list[Transaction]:
        """Get transaction with filter.

        Parameters
        ----------
        database : CryptoDatabase
            The database connection
        kwargs :
           Keywords arguments passed to Transaction.from_filter method 

        Returns
        -------
        list[Transaction] : Transactions which match with the filter.

        """
        return Transaction.from_filter(self.id, database, **kwargs)

    def load_currencies(self, database: CryptoDatabase):
        """Load currencies and amount of this portfolio. \
                Initialize `self.currencies`.

        Parameters
        ----------
        database : CryptoDatabase
           The database connection 
        """
        # Juste un raccourcies pour éviter d'avori des lignes trop longues.
        # (Reference copy)
        CRYPTOS = Cryptocurrency.CRYPTOCURRENCIES
        for result in database.get_currencies_portfolios(self.id):
            id_ = result['idCurrency']
            if result['isCrypto'] and id_ not in CRYPTOS.keys():
                self.currencies[Cryptocurrency.from_db_dict(result)] = result['amount']
            elif not result['isCrypto']:
                self.currencies[Currency.CURRENCIES[id_]] = result['amount']
            else:
                self.currencies[CRYPTOS[id_]] = result['amount']

    def upload_currencies_in_db(self, database: CryptoDatabase):
        """Save `self.currencies` dictionary in the database.

        Parameters
        ----------
        database : CryptoDatabase
           The database connection 
        """
        for currency, amount in self.currencies.items():
            try:
                database.insert_currency_portfolio(
                    self.id, currency.id, amount, commit=False)
            except Exception as e:
                print(e)
                database.update_currency_portfolio(
                    self.id, currency.id, amount, commit=False)
        database.commit()

    def add_transaction(self, /,
                        send: tuple[Currency, float],
                        received: tuple[Currency, float],
                        database: CryptoDatabase,
                        date: datetime = None):
        """Add a new transaction for this portfolio.

        Parameters
        ----------
        send : tuple[Currency, float]
           The currency send and the amount corresponding (spent) 
        received : tuple[Currency, float]
           The currency received and the amount corresponding 
        database : CryptoDatabase
           The database connection 
        date : datetime, optional
           The datetime of this transaction. Default: current datetime.
        """
        if date is None:
            date = datetime.now()
        Transaction.new_transaction(send, received, date, self.id, database)

        if send[0] in self.currencies.keys():
            self.currencies[send[0]] -= send[1]
        else:
            self.currencies[send[0]] = -send[1]

        if received[0] in self.currencies.keys():
            self.currencies[received[0]] -= received[1]
        else:
            self.currencies[received[0]] = received[1]

    def update(self, database: CryptoDatabase):
        """Update this portfolio in database with current name and password atrtibutes.

        Parameters
        ----------
        database : CryptoDatabase
            The database connection
        """
        database.update_portfolio(self.to_dict())

    def delete(self, database: CryptoDatabase):
        """Delete the portfolio from the database.

        Parameters
        ----------
        database : CryptoDatabase
            The database connection
        """
        database.delete_portfolio(self.id)

    def to_dict(self) -> dict:
        """Returns portfolio data in a dictionary.

        Returns
        -------
        dict : Portfolio's data
        """
        return {
            'id': self.id,
            'name': self.name,
            'password': self.password
        }

    @classmethod
    def new_portfolio(cls, name: str, password: str, database: CryptoDatabase):
        """Create a new portfolio in database.

        Parameters
        ----------
        name : str
            The name of new portfolio
        password : str
            The password of the portfolio
        database : CryptoDatabase
            The database connection
        """
        id_ = database.insert_portfolio(dict(name=name, password=password))
        return cls(id_, name, password)

    @classmethod
    def get_all_portfolios(cls, database: CryptoDatabase) -> list:
        """Returns all portfolios from the database.

        Parameters
        ----------
        database : CryptoDatabase
           The database connection 

        Returns
        -------
        list[Portfolio] : The list of portfolio
        """
        return [
            cls(result['idPortfolio'], result['name'], result['password'])
            for result in database.get_portfolios()
        ]

    @classmethod
    def from_db(cls, id_: int, database: CryptoDatabase):
        """Get and create an instance from id and database.

        Parameters
        ----------
        id_ : int
           portfolio's id to get 
        database : CryptoDatabase
           The database connection 
        """
        result = database.get_portfolio_by_id(id_)
        if result is not None:
            return cls(id_, result['name'], result['password'])

