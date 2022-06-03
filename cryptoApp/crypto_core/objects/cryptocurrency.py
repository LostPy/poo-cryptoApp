from datetime import datetime
from pathlib import Path
import shutil
import __main__  # to get the path of __main__ (Python file executed)

import requests

from .. import crypto_api
from ..db import CryptoDatabase
from . import Currency


class Cryptocurrency(Currency):
    """All the informations concerning the crypto we want to look at"""

    CRYPTOCRYPTOCURRENCIES = dict()  # A dictionary with currencies already loaded
    LOGO_DIR_PATH = Path(__main__.__file__).resolve().parent / 'logos'
    LOGO_FILENAME_FORMAT = "{id}.png"

    def __init__(self, id_: str, name: str, ticker: str, *,
                 price: float = None,
                 circulating_supply: int = None,
                 rank: int = None):
        super(Cryptocurrency, self).__init__(name, id_)
        self.ticker = ticker
        self.price = price
        self.circulating_supply = circulating_supply
        self.rank = rank
        self.last_update = None

    @property
    def logo(self):
        """Path of the logo, returns None if there is not \
        logo avaible for this cryptocurrency.
        """
        path = self.logo_path(self.id)
        if path.exists():
            return path
        return None

    def get_price_change(self, vs_currency: Currency):
        """Returns the evolution of the price during last 24h.
        """
        return crypto_api.get_price_change(self.id, vs_currency.id)

    def get_market_chart(self, vs_currency: Currency, days: int) -> 'pandas.DataFrame':
        """Get the evolution on last days"""
        return crypto_api.get_market_chart(self.id, vs_currency.id, days)

    def get_market_chart_by_range(self,
                                  vs_currency: Currency,
                                  start: datetime,
                                  end: datetime) -> 'pandas.DataFrame':
        """Get the evolution of the price between two datetime"""
        return crypto_api.get_market_chart_by_range(self.id,
                                                    vs_currency.id,
                                                    start.timestamp(),
                                                    end.timestamp())

    def _update_from_api_dict(self, d: dict):
        self.name = d['name']
        self.ticker = d['symbol']
        self.price = d['current_price']
        self.circulating_supply = int(d['circulating_supply'])
        self.rank = d['market_cap_rank']
        self.last_update = datetime.now()
        return self

    def update(self):
        """Update data from the api"""
        data = crypto_api.get_coin_by_id(self.id)
        self._update_from_api_dict(data)

    def update_db(self, database: CryptoDatabase, commit: bool = True):
        """Update database for this cryptocurrency with current attributes.
        """
        database.update_currency(self.to_dict(), commit=commit)

    def delete(self, database: CryptoDatabase, commit: bool = True):
        """Delete this cryptocurrency from the database."""
        database.delete_currencies([self.id], commit=commit)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'ticker': self.ticker,
            'price': self.price,
            'logo': self.logo_path(self.id),
            'circulating_supply': self.circulating_supply,
            'rank': self.rank,
            'is_crypto': True
        }

    @classmethod
    def from_db_dict(cls, d: dict, add_to_cryptos_dict: bool = True):
        currency = cls(
            d['idCurrency'],
            name=d['name'],
            ticker=d['ticker'],
            price=d['price'],
            circulating_supply=d['circulatingSupply'],
            rank=d['rank']
        )
        if add_to_cryptos_dict:
            cls.CRYPTOCURRENCIES[currency.id] = currency
        return currency

    @classmethod
    def from_api_dict(cls, d: dict):
        logo_path = cls.logo_path(d['id'])
        if not logo_path.exists():
            # if logo_path doesn't exists, this function download the image
            # stream to guarantee no interruptions
            r = requests.get(d['image'], stream=True)
            r.raw.decode_content = True  # To don't have a image file's size to 0
            with open(logo_path, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

        return cls(
            d['id'],
            name=d['name'],
            ticker=d['symbol'],
            price=d['current_price'],
            circulating_supply=int(d['circulating_supply']),
            rank=d['market_cap_rank']
        )

    @classmethod
    def from_api(cls, id_: str, database: CryptoDatabase = None):
        """Get a new cryptocurrency from API.
        If database is not None, this cryptocurrency is saved in database.
        """
        if id_ in cls.CRYPTOCURRENCIES.keys():
            cls.CRYPTOCURRENCIES[id_].update()
            return cls.CRYPTOCURRENCIES[id_]

        currency = cls.from_api_dict(crypto_api.get_coin_by_id(id_))
        if database is not None:
            cls.add_currencies_to_db([currency], database)
        return currency

    @classmethod
    def get_top_coins_market(cls, vs_currency: Currency,
                             max_rank: int = 10,
                             database: CryptoDatabase = None) -> list:
        """Get a top cryptocurrency from API.
        If database is not None, this cryptocurrency is saved in database.
        """
        # just a shortcup to don't have lines too long
        # (Reference copy)
        CURRENCIES = cls.CRYPTOCURRENCIES
        currencies = [
            cls.from_api_dict(currency_data)
            if currency_data['id'] not in CURRENCIES
            else CURRENCIES[currency_data['id']]._update_from_api_dict(currency_data)
            for currency_data in crypto_api.get_top_cryptocurrencies(
                vs_currency.id, max_rank)
        ]

        if database is not None:
            cls.add_currencies_to_db(currencies, database)

        return currencies

    @classmethod
    def from_db(cls, id_: str, database: CryptoDatabase):
        if id_ in cls.CRYPTOCURRENCIES.keys():
            return cls.CRYPTOCURRENCIES[id_]

        result = database.get_currency_by_id(id_.lower())
        if result is not None:
            return cls.from_db_dict(result)

    @classmethod
    def add_currencies_to_db(cls, currencies: list, database: CryptoDatabase):
        """Add existing currencies to the database.\
        Use for currencies created from API."""
        database.insert_currencies([currency.to_dict() for currency in currencies])

    @classmethod
    def init_cryptocurrencies(cls, database: CryptoDatabase, rank_max: int = 10):
        """Initialize `cls.CRYPTOCURRENCIES` dictionary with top cryptocurrencies.
        """
        cls.CRYPTOCURRENCIES = {
            d['idCurrency']: cls.from_db_dict(d, add_to_cryptos_dict=False)
            for d in database.get_top_cryptocurrencies()
        }

    @classmethod
    def update_db_cryptocurrencies(cls, database: CryptoDatabase):
        """Update database data for all cryptocurrencies from `cls.CRYPTOCURRENCIES`.
        """
        for currency in cls.CRYPTOCURRENCIES.values():
            currency.update_db(database, commit=False)
        database.commit()

    @classmethod
    def multi_delete(cls,
                     currencies: list,
                     database: CryptoDatabase,
                     commit: bool = True):
        """Delete a list of cryptocurrencies from the database."""
        database.delete_currencies([c.id for c in currencies], commit=commit)

    @classmethod
    def logo_path(cls, id_: str):
        """Returns the logo path for currency id given."""
        return cls.LOGO_DIR_PATH / cls.LOGO_FILENAME_FORMAT.format(id_)
