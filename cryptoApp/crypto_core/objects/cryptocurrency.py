from datetime import datetime
from pathlib import Path
import shutil
import __main__  # Pour récupérer le path du __main__ (Fichier python executé)

import requests

from .. import crypto_api
from ..db import CryptoDatabase
from .. import errors
from . import Currency


class Cryptocurrency(Currency):
    """All the informations concerning the crypto we want to look at.

    Attributes
    ----------
    price : float
        The price of crypto
    circulating_supply : int
        Circulating supply for this crypto
    rank : int
        The rank of this crypto
    last_update : datetime.datetime
        datetime of last update crypto's data.

    Properties
    ----------
    logo : Path | None
        Returns the path of crypto's logo if this logo exists.

    Class attributes
    ----------------
    CRYPTOCURRENCIES : dict[str, Cryptocurrency]
        A dictionary with all cryptocurrency already loaded.
    LOGO_DIR_PATH : pathlib.Path
        The directory path for crypto's logos.
    LOGO_FILENAME_FORMAT : str
        The format of filename for crypto's logo.
    """

    CRYPTOCURRENCIES = dict()  # Un dictionnaire avec les cryptomonaies déjà chargées
    LOGO_DIR_PATH = Path(__main__.__file__).resolve().parent / 'logos'
    LOGO_FILENAME_FORMAT = "{id}.png"

    def __init__(self, id_: str, name: str, ticker: str, *,
                 price: float = None,
                 circulating_supply: int = None,
                 last_update: datetime = None,
                 rank: int = None):
        """__init__.

        Parameters
        ----------
        id_ : str
           Cryptocurrency's id. 
        name : str
           Cryptocurrency's name. 
        ticker : str
           Cryptocurrency's ticker. 
        price : float
           price of crypto 
        circulating_supply : int
            circulating supply of crypto.
        last_update : datetime
           datetime of last update of currency 
        rank : int
            rank of the crypto on CoinGecko API.
        """
        super().__init__(id_, name, ticker)
        self.price = price
        self.circulating_supply = circulating_supply
        self.rank = rank
        self.last_update = last_update

    @property
    def gecko_id(self) -> str:
        """Redefine gecko_id property, it's the same id than database.
        
        Returns
        -------
        str : id for CoinGecko API
        """
        return self.id

    @property
    def logo(self):
        """Path of the logo, returns None if there is not \
        logo avaible for this cryptocurrency.

        Returns
        -------
        Path | None : path of the logo.
        """
        path = self.logo_path(self.id)
        if path.exists():
            return path
        return None

    def get_price_change(self, vs_currency: Currency):
        """Returns the evolution of the price during last 24h.

        Parameters
        ----------
        vs_currency : Currency
            The fiat currency

        Returns
        -------
        float : The price change from API.
        """
        return crypto_api.get_price_change(self.id, vs_currency.id)

    def get_market_chart(self, vs_currency: Currency, days: int) -> 'pandas.DataFrame':
        """Get the evolution on last days
        
        Parameters
        ----------
        vs_currency : Currency
            The fiat currency
        days : int
            Get data from D - days to D with D the current datetime.

        Returns
        -------
        pandas.DataFrame : price evolution of currency in a table.
        """
        return crypto_api.get_market_chart(self.id, vs_currency.gecko_id, days)

    def get_market_chart_by_range(self,
                                  vs_currency: Currency,
                                  start: datetime,
                                  end: datetime) -> 'pandas.DataFrame':
        """Get the evolution of the price between two datetime.

        Parameters
        ----------
        vs_currency : Currency
            The fiat currency.
        start : datetime.datetime
            The early datetime to get data
        end : datetime.datetime
            The lastest datetime to get data

        Returns
        -------
        pandas.DataFrame : price evolution of currency in a table.
        """
        return crypto_api.get_market_chart_by_range(self.id,
                                                    vs_currency.id,
                                                    start.timestamp(),
                                                    end.timestamp())

    def _update_from_api_dict(self, d: dict):
        """Update data from a dictionary got with API.

        Parameters
        ----------
        d : dict
            dictionary with data from API.
        """
        self.name = d['name']
        self.ticker = d['ticker']
        self.price = d['price']
        self.circulating_supply = int(d['circulating_supply'])
        self.rank = d['rank']
        self.last_update = datetime.now()
        return self

    def update(self):
        """Update data from the api."""
        data = crypto_api.get_coin_by_id(self.id)
        self._update_from_api_dict(data)

    def update_db(self, database: CryptoDatabase, commit: bool = True):
        """Update database for this cryptocurrency with current attributes.

        Parameters
        ----------
        database : CryptoDatabase
            The database connection
        commit : bool, optional
            If True, commit the update. Default: True.
        """
        database.update_currency(self.to_dict(), commit=commit)

    def delete(self, database: CryptoDatabase, commit: bool = True):
        """Delete this cryptocurrency from the database.
        
        Parameters
        ----------
        database : CryptoDatabase
            The database connection.
        commit : bool, optional
            If True, commit changement. Default: True.
        """
        database.delete_currencies([self.id], commit=commit)

    def to_dict(self) -> dict:
        """Returns data of currency in a dictionary.

        Returns
        -------
        dict : The dictionary with currency's data.
        """
        return {
            'id': self.id,
            'name': self.name,
            'ticker': self.ticker,
            'price': self.price,
            'logo': self.logo_path(self.id),
            'circulating_supply': self.circulating_supply,
            'last_update': self.last_update,
            'rank': self.rank,
            'is_crypto': True
        }

    @classmethod
    def from_db_dict(cls, d: dict, add_to_cryptos_dict: bool = True):
        """Create an instance of Cryptocurrency from a dictionary with database format.

        Parameters
        ----------
        d : dict
           The dictionary with data get from database. 
        add_to_cryptos_dict : bool, optional
           If True, add cryptocurrencies to the `cls.CRYPTOCURRENCIES` dict, \
                   default: True.

        Returns
        -------
        Cryptocurrency : The new instance
        """
        currency = cls(
            d['idCurrency'],
            name=d['name'],
            ticker=d['ticker'],
            price=d['price'],
            circulating_supply=d['circulatingSupply'],
            last_update=d['last_update'],
            rank=d['rank']
        )
        if add_to_cryptos_dict:
            cls.CRYPTOCURRENCIES[currency.id] = currency
        return currency

    @classmethod
    def from_api_dict(cls, d: dict, add_to_cryptos_dict: bool = True):
        """Create an instance from a dictionary with data from API.

        Parameters
        ----------
        d : dict
           The dictionary with data get from API. 
        add_to_cryptos_dict : bool
           If True, add cryptocurrencies to the `cls.CRYPTOCURRENCIES` dict, \
                   default: True.

        Returns
        -------
        Cryptocurrency : The new instance
        """
        logo_path = cls.logo_path(d['id'])
        if not logo_path.exists():
            # if logo_path doesn't exists, this function download the image
            # stream to guarantee no interruptions
            r = requests.get(d['image'], stream=True)
            r.raw.decode_content = True  # To don't have a image file's size to 0
            with open(logo_path, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

        currency = cls(
            d['id'],
            name=d['name'],
            ticker=d['ticker'],
            price=d['price'],
            circulating_supply=int(d['circulating_supply']),
            last_update=datetime.now(),
            rank=d['rank']
        )
        if add_to_cryptos_dict:
            cls.CRYPTOCURRENCIES[currency.id] = currency
        return currency

    @classmethod
    def from_api(cls, id_: str, vs_currency: Currency, database: CryptoDatabase = None):
        """Get a new cryptocurrency from API.
        If database is not None, this cryptocurrency is saved in database.

        Parameters
        ----------
        id_ : str
            Cryptocurrency's id to get with API.
        vs_currency : Currency
            The fiat currency to use as unit for price...
        database : CryptoDatabase, optional
            The database connection. If not None, add cryptocurrency to the database. \
                    By default: None.

        Returns
        -------
        Cryptocurrency : The new instance
        """
        if id_ in cls.CRYPTOCURRENCIES.keys():
            cls.CRYPTOCURRENCIES[id_].update()
            return cls.CRYPTOCURRENCIES[id_]

        try:
            currency = cls.from_api_dict(crypto_api.get_coin_by_id(id_, vs_currency.gecko_id))
        except errors.ApiCurrencyNotFound:
            raise errors.CurrencyApiNotFound(id_)

        if database is not None:
            cls.add_currencies_to_db([currency], database)
        return currency

    @classmethod
    def get_top_coins_market(cls, vs_currency: Currency,
                             max_rank: int = 10,
                             database: CryptoDatabase = None) -> list:
        """Get a top cryptocurrency from API.
        If database is not None, this cryptocurrency is saved in database.

        Parameters
        ----------
        vs_currency : Currency
            The fiat currency.
        max_rank : int, optional
            The max rank to get in top, default: 10.
        database : CryptoDatabase, optional
            The database connection, if not None, save crypto in database. Default: None.

        Returns
        -------
        list[Cryptocurrency] : The top currencies.
        """
        # Juste un raccourci pour ne pas avoir des lignes trop longues.
        # (Reference copy)
        CURRENCIES = cls.CRYPTOCURRENCIES
        currencies = [
            cls.from_api_dict(currency_data)
            if currency_data['id'] not in CURRENCIES
            else CURRENCIES[currency_data['id']]._update_from_api_dict(currency_data)
            for currency_data in crypto_api.get_top_coins_market(
                vs_currency.gecko_id, max_rank)
        ]

        if database is not None:
            cls.add_currencies_to_db(currencies, database, ignore=True)

        return currencies

    @classmethod
    def from_db(cls, id_: str, database: CryptoDatabase):
        """Create an instance from database with id.

        Parameters
        ----------
        id_ : str
           The currency's id. 
        database : CryptoDatabase
           The connection to database. 

        Returns
        -------
        Cryptocurrency : The new instance

        Raises
        ------
        errors.CurrencyDbNotFound : raised if id_ does not exist in the database.
        """
        if id_ in cls.CRYPTOCURRENCIES.keys():
            return cls.CRYPTOCURRENCIES[id_]
        result = database.get_currency_by_id(id_.lower())
        if result is not None:
            return cls.from_db_dict(result)
        raise errors.CurrencyDbNotFound(id_)

    @classmethod
    def add_currencies_to_db(cls, currencies: list, database: CryptoDatabase,
                             ignore: bool = False):
        """Add existing currencies to the database.\
        Use for currencies created from API.

        Parameters
        ----------
        currencies : list[Currency]
            The list of currency to add in database.
        database : CryptoDatabase
            The connection to database.
        ignore : bool, optional
            If True, ignore currencies which already exists in database. Default: False.
        """
        database.insert_currencies(
            [currency.to_dict() for currency in currencies], ignore=ignore)

    @classmethod
    def init_cryptocurrencies(cls, database: CryptoDatabase, rank_max: int = 10):
        """Initialize `cls.CRYPTOCURRENCIES` dictionary with top cryptocurrencies.

        Parameters
        ----------
        database : CryptoDatabase
            The connection to database
        rank_max : int, optional
            The max rank to get in top currencies. Default: 10.
        """
        cls.CRYPTOCURRENCIES = {
            d['idCurrency']: cls.from_db_dict(d, add_to_cryptos_dict=False)
            for d in database.get_top_cryptocurrencies(rank_max)
        }

    @classmethod
    def update_db_cryptocurrencies(cls, database: CryptoDatabase):
        """Update database data for all cryptocurrencies from `cls.CRYPTOCURRENCIES`.

        Parameters
        ----------
        database : CryptoDatabase
            The database connection.
        """
        for currency in cls.CRYPTOCURRENCIES.values():
            currency.update_db(database, commit=False)
        database.commit()

    @classmethod
    def multi_delete(cls,
                     currencies: list,
                     database: CryptoDatabase,
                     commit: bool = True):
        """Delete a list of cryptocurrencies from the database.
         
        Parameters
        ----------
        currencies : list[Currency]
            The list of currency to delete (in database)
        database : CryptoDatabase
            The database connection.
        commit : bool, optional
            If True, commit changement. Default: True.
        """
        database.delete_currencies([c.id for c in currencies], commit=commit)

    @classmethod
    def logo_path(cls, id_: str) -> Path:
        """Returns the logo path for currency id given.

        Parameters
        ----------
        id_ : str
            Currency's ID

        Returns
        -------
        Path : The path of logo.
        """
        return cls.LOGO_DIR_PATH / cls.LOGO_FILENAME_FORMAT.format(id=id_)
