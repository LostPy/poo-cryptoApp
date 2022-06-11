"""Class to define a currency
"""
from ..db import CryptoDatabase
from . import NameableObject


class Currency(NameableObject):
    """Define the currency.

    Attributes
    ----------
    ticker : str
        The ticker (symbol) of the currency.

    Properties
    ----------
    gecko_id : str
        The id of currency on CoinGecko API.

    Class attributes
    ----------------
    CURRENCIES : dict[str, Currency]
        A dictionary to stock currency already loaded.
        Keys are currencies's id and value the currencies themself.

    Classmethods
    ------------
    init_currencies : None
        Initialize `Currency.CURRENCIES`
    """

    CURRENCIES = dict()

    def __init__(self, id_: int, name: str, ticker: str):
        """__init__.

        Parameters
        ----------
        id_ : int
           Currency's id 
        name : str
           Currency's name 
        ticker : str
           Currency's ticker 
        """
        super().__init__(id_, name)
        self.ticker = ticker

    @property
    def gecko_id(self) -> str:
        """id of currency use for coingecko API."""
        return self.ticker.lower()

    @classmethod
    def init_currencies(cls, database: CryptoDatabase):
        """Initialize Currency.CURRENCIES dictionary.

        Parameters
        ----------
        database : CryptoDatabase
           Instance of CryptoDatabase to get currencies. 
        """
        cls.CURRENCIES = {
            d['idCurrency']: Currency(d['idCurrency'], d['name'], d['ticker'])
            for d in database.get_currencies(where="WHERE isCrypto=?", where_args=(0, ))
        }
