from datetime import datetime

from . import Cryptocurrency, Transaction
from . import NameableObject
from ..db import CryptoDatabase


class Portofolio(NameableObject):
    """Define a portofolio of an user with the list of transactions.
    """

    def __init__(self, id_: int, name: str, password: str):
        super().__init__(id_, name)
        self.password: str = password
        self.currencies = dict()

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
        self.currencies = {
            Cryptocurrency.from_db_dict(result): result['amount']
            for result in database.get_currencies_portofolios(self.id)
        }

    def upload_currencies_in_db(self, database: CryptoDatabase):
        for currency, amount in self.currencies:
            database.update_currency_portofolio(
                self.id, currency.id, amount, commit=False)
        database.commit()

    @classmethod
    def new_portofolio(cls, name: str, password: str, database: CryptoDatabase):
        """Create a new portofolio in database.
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
