from pycoingecko import CoinGeckoAPI
import pandas as pd


cg = CoinGeckoAPI()


def get_price(name, money):
    return cg.get_price(ids=name, vs_currencies=money)


def get_price_change(name, money):
    return cg.get_price(ids=name, vs_currencies=money, include_24hr_change=True)


def get_trending():
    return cg.get_search_trending()['coins']


def get_defi():
    return cg.get_global_decentralized_finance_defi()


def get_categories():
    return cg.get_coins_categories_list()


# Utilisateur va mettre l'intervalle et le nb de jours pour visualiser l'évolution de la crypto choisie
def get_market_chart(name, money, time):
    market_chart = cg.get_coin_market_chart_by_id(id=name,vs_currency=money,days=time)
    return pd.DataFrame(market_chart['prices'], columns=['date', 'price'])   


def get_market_chart_by_range(name, money, start, end):
    market_chart = cg.get_coin_market_chart_range_by_id(id=name, vs_currency=money, from_timestamp=start, to_timestamp=end)
    return pd.DataFrame(market_chart['prices'], columns=['date', 'price'])
