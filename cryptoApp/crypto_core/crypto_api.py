import requests
from pycoingecko import CoinGeckoAPI
import pandas as pd

from .errors import ApiConnectionError, ApiRequestsError, ApiCurrencyNotFound


cg = CoinGeckoAPI()


def ping():
    try:
        return cg.ping()
    except requests.ConnectionError:
        raise ApiConnectionError()


def get_coin_by_id(name: str, vs_currency: str):
    try:
        result = cg.get_coin_by_id(id=name,
                                   localization=False,
                                   tickers=False,
                                   community_data=False,
                                   developer_data=False)
        return {
            'id': result['id'],
            'name': result['name'],
            'ticker': result['symbol'],
            'image': result['image']['large'],
            'rank': result['market_cap_rank'],
            'price': result['market_data']['current_price'][vs_currency.lower()],
            'circulating_supply': result['market_data']['circulating_supply']
        }
    except requests.ConnectionError:
        raise ApiConnectionError()

    except ValueError:
        raise ApiCurrencyNotFound(name)

    except KeyError:
        raise ApiCurrencyNotFound(vs_currency)


def get_top_coins_market(money: str, max_rank: int = 10) -> list[dict]:
    try:
        if not isinstance(max_rank, int) and not (1 <= max_rank <= 100):
            raise ValueError(f"max_rank must be an integer between 1 and 100, not '{max_rank}'")
        result = cg.get_coins_markets(vs_currency=money.lower(), per_page=max_rank)
        return [
            {
                'id': currency['id'],
                'name': currency['name'],
                'ticker': currency['symbol'],
                'image': currency['image'],
                'rank': currency['market_cap_rank'],
                'price': currency['current_price'],
                'circulating_supply': currency['circulating_supply']
            }
            for currency in result
        ]
    except requests.ConnectionError:
        raise ApiConnectionError()

    except ValueError:
        raise ApiCurrencyNotFound(money)


def get_price(name, money):
    try:
        name = name.lower()
        money = money.lower()
        return cg.get_price(ids=name, vs_currencies=money)[name][money]
    except requests.ConnectionError:
        raise ApiConnectionError()

    except ValueError:
        raise ApiCurrencyNotFound(name)

    except KeyError:
        raise ApiCurrencyNotFound(money)


def get_price_change(name, money):
    try:
        name = name.lower()
        money = money.lower()
        result = cg.get_price(ids=name,
                              vs_currencies=money,
                              include_24hr_change=True)
        return result[name][f'{money}_24h_change']
    except requests.ConnectionError:
        raise ApiConnectionError()

    except ValueError:
        raise ApiCurrencyNotFound(name)
    
    except KeyError:
        raise ApiCurrencyNotFound(money)


def get_trending():
    try:
        return cg.get_search_trending()['coins']
    except requests.ConnectionError:
        raise ApiConnectionError()


def get_defi():
    try:
        return cg.get_global_decentralized_finance_defi()
    except requests.ConnectionError:
        raise ApiConnectionError()



def get_categories():
    try:
        return cg.get_coins_categories_list()
    except requests.ConnectionError:
        raise ApiConnectionError()


# Utilisateur va mettre l'intervalle et le nb de jours pour visualiser l'évolution de la crypto choisie
def get_market_chart(name, money, time):
    try:
        market_chart = cg.get_coin_market_chart_by_id(id=name, vs_currency=money, days=time)
        return pd.DataFrame(market_chart['prices'], columns=['date', 'price'])   

    except requests.ConnectionError:
        raise ApiConnectionError()

    except ValueError as e:
        # Vérifie que le mesage d'erreur correspond à une erreur venant de 'vs_currency' (money)
        if str(e)[10:-1].strip("'") == "invalid vs_currency":
            raise ApiCurrencyNotFound(money)
        raise ApiCurrencyNotFound(name)


def get_market_chart_by_range(name, money, start, end):
    try:
        market_chart = cg.get_coin_market_chart_range_by_id(id=name, vs_currency=money, from_timestamp=start, to_timestamp=end)
        return pd.DataFrame(market_chart['prices'], columns=['date', 'price'])
    except requests.ConnectionError:
        raise ApiConnectionError()

