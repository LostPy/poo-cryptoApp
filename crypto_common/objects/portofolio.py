from datetime import datetime

from . import Cryptocurrency, Transaction


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
