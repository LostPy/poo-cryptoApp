from datetime import datetime

from . import Cryptocurrency, Transaction
from ..db import CryptoDatabase


class Portofolio:
    """Define a portofolio of an user with the list of transactions.
    """

    def __init__(self, id_: int, name: str, password: str):
        self.id: int = id_
        self.name: int = name
        self.password: int = password

    def get_transactions(self, start: datetime, end: datetime) -> list[Transaction]:
        pass

    def get_transaction_by_id(self, id_: int) -> Transaction:
        pass

    def get_transaction_by_crypto(crypto: Cryptocurrency) -> Cryptocurrency:
        pass

    @classmethod
    def from_db(cls, id_: int, database: CryptoDatabase):
        result = database.get_portofolio_by_id(id_)
        if result is not None:
            return cls(id_, result['name'], result['password'])
