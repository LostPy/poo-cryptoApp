import os.path
import sys
sys.path.append(os.path.abspath("../poo-crypto-common/cryptoApp"))
print(sys.path)

from crypto_core.crypto_api import *
import matplotlib.pyplot as plt
from datetime import datetime


def test_market_chart():
    market_chart = get_market_chart('bitcoin', 'usd', '3')
    market_chart_by_range = get_market_chart_by_range('bitcoin', 'usd', '1651356000', '1652345026') # du 1er mai à mnt (12/05)
    plt.subplot(2, 1, 1)
    plt.plot(market_chart['date'], market_chart['price'])
    plt.grid()
    plt.subplot(2, 1, 2)
    plt.plot(market_chart_by_range['date'], market_chart_by_range['price'])
    plt.grid()
    plt.show()


def test_get_trending():
    print(get_trending())


def test_coin_by_id():
    print(get_coin_by_id('bitcoin', 'eur'))


def test_bad_id():
    print(get_coin_by_id('bitsdfscoin', 'eur'))  # raise an ApiCurrencyNotFound
    #get_market_chart('bitcoin', 'aezet', 7)  # raise an ApiCurrencyNotFound


if __name__ == '__main__':
    test_coin_by_id()
