from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

""" All the functions that'll be used for the other files """

def get_price(name, money):
	return cg.get_price(ids=name, vs_currencies=money)

def get_price_change(name, money):
	return cg.get_price(ids=name, vs_currencies=money, include_24hr_change=True)

def get_trending():
	return cg.get_search_trending()

def get_defi():
	return cg.get_global_decentralized_finance_defi()

def get_categories():
	return cg.get_coins_categories_list()

