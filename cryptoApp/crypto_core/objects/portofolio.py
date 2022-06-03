from datetime import datetime

from . import Currency, Cryptocurrency, Transaction
from . import NameableObject
from ..db import CryptoDatabase


class Portofolio(NameableObject):
    """Define a portofolio of an user with the list of transactions.
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

    def get(self, currency: Cryptocurrency) -> float:
        """Returns `self.currencies.get(currency)`."""
        if not isinstance(currency, Cryptocurrency):
            raise ValueError("The key must be an instance of Cryptocurrency")
        return self.currencies.get(currency)

    def get_transactions(self,
                         database: CryptoDatabase,
                         start: datetime = None,
                         end: datetime = None) -> list[Transaction]:
        if start is None and end is None:
            range_date = None
        else:
            range_date = (start, end)
        return Transaction.from_filter(self.id, database, range_date=range_date)

    def get_transactions_filtered(self,
                                  database: CryptoDatabase,
                                  **kwargs) -> list[Transaction]:
        return Transaction.from_filter(self.id, database, **kwargs)

    def load_currencies(self, database: CryptoDatabase):
        """Load currencies and amount from database."""
        # just a shortcup to don't have lines too long and for lisibility
        # (Reference copy)
        CRYPTOS = Cryptocurrency.CRYPTOCURRENCIES
        self.currencies = {
            Cryptocurrency.from_db_dict(result)
            if result['idCurrency'] not in CRYPTOS.keys()
            else CRYPTOS[result['idCurrency']]: result['amount']
            for result in database.get_currencies_portofolios(self.id)
        }

    def upload_currencies_in_db(self, database: CryptoDatabase):
        for currency, amount in self.currencies:
            database.update_currency_portofolio(
                self.id, currency.id, amount, commit=False)
        database.commit()

    def add_transaction(self, /,
                        send: tuple[Currency, float],
                        received: tuple[Currency, float],
                        database: CryptoDatabase,
                        date: datetime = None):
        if date is None:
            date = datetime.now()
        Transaction.new_transaction(send, received, date, self.id, database)

    def update(self, database: CryptoDatabase):
        """Update this portfolio in database with current name and password atrtibutes.
        """
        database.update_portofolio(self.to_dict())

    def delete(self, database: CryptoDatabase):
        """Delete the portfolio from the database."""
        database.delete_portofolio(self.id)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'password': self.password
        }

    @classmethod
    def new_portofolio(cls, name: str, password: str, database: CryptoDatabase):
        """Create a new portfolio in database.
        """
        id_ = database.insert_portofolio(dict(name=name, password=password))
        return cls(id_, name, password)

    @classmethod
    def get_all_portofolios(cls, database: CryptoDatabase) -> list:
        return [
            cls(result['idPortofolio'], result['name'], result['password'])
            for result in database.get_portofolios()
        ]

    @classmethod
    def from_db(cls, id_: int, database: CryptoDatabase):
        result = database.get_portofolio_by_id(id_)
        if result is not None:
            return cls(id_, result['name'], result['password'])
