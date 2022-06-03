from pycoingecko import CoinGeckoAPI
import pandas as pd


cg = CoinGeckoAPI()


def get_coin_by_id(name: str, vs_currency: str):
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
        'market_cap_rank': result['market_cap_rank'],
        'current_price': result['market_data']['current_price'][vs_currency.lower()],
        'circulating_supply': result['market_data']['circulating_supply']
    }


def get_top_coins_market(money: str, max_rank: int = 10) -> list[dict]:
    if not isinstance(max_rank, int) and not (1 <= max_rank <= 100):
        raise ValueError(f"max_rank must be an integer between 1 and 100, not '{max_rank}'")
    result = cg.get_coins_market(vs_currencies=money.lower(), per_page=max_rank)
    return {
        'id': result['id'],
        'name': result['name'],
        'ticker': result['symbol'],
        'image': result['image'],
        'market_cap_rank': result['market_cap_rank'],
        'current_price': result['current_price'],
        'circulating_supply': result['circulating_supply']
    }


def get_price(name, money):
    name = name.lower()
    money = money.lower()
    return cg.get_price(ids=name, vs_currencies=money)[name][money]


def get_price_change(name, money):
    name = name.lower()
    money = money.lower()
    result = cg.get_price(ids=name,
                          vs_currencies=money,
                          include_24hr_change=True)
    return result[name][f'{money}_24h_change']


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
