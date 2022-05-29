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

    def get_transactions(self, start: datetime, end: datetime) -> list[Transaction]:
        pass

    def get_transaction_by_id(self, id_: int) -> Transaction:
        pass

    def get_transaction_by_crypto(crypto: Cryptocurrency) -> Cryptocurrency:
        pass

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
