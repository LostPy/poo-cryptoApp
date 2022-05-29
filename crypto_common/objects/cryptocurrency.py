
from crypto_common.crypto_api import get_trending
from crypto_common.db import CryptoDatabase
from . import Currency


class Cryptocurrency(Currency):
    """All the informations concerning the crypto we want to look at"""

    def __init__(self, id, name, ticker, price, logo, circulating_supply, rank):
        super(Cryptocurrency, self).__init__(name, id)
        self.ticker = ticker
        self.price = price
        self.logo = logo
        self.circulating_supply = circulating_supply
        self.rank = rank

    def get_price_change(self, delay):
        """Function to get the evolution of the price during a delay: \
        like one week, one day.
        """
        pass

    def get_price_change_year(self):
        """Get the evolution of the price on 1 year"""
        pass

    def update_data(self):
        """The new data from the api is gonna be updated in the arguments"""
        pass

    @classmethod
    def get_trending(cls):
        pass

    @classmethod
    def from_db(cls, id_: str, database: CryptoDatabase):
        result = database.get_currency_by_id(id_.lower())
        if result is not None:
            return cls(
                result['idCurrency'],
                name=result['name'],
                ticker=result['ticker'],
                price=result['price'],
                logo=result['logo'],
                circulating_supply=result['circulatingSupply'],
                rank=result['rank']
            )
