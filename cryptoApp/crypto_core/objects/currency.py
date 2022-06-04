"""Class to define a currency
"""
from ..db import CryptoDatabase
from . import NameableObject


class Currency(NameableObject):
    """Define the currency"""

    CURRENCIES = dict()

    def __init__(self, id_: int, name: str, ticker: str):
        super().__init__(id_, name)
        self.ticker = ticker

    @property
    def gecko_id(self) -> str:
        """id of currency use for coingecko API."""
        return self.ticker.lower()

    @classmethod
    def init_currencies(cls, database: CryptoDatabase):
        """Initialize `cls.CURRENCIES` dictionary with currencies (not crypto).
        """
        cls.CURRENCIES = {
            d['idCurrency']: Currency(d['idCurrency'], d['name'], d['ticker'])
            for d in database.get_currencies(where="WHERE isCrypto=?", where_args=(0, ))
        }
