from . import currency


class Cryptocurrency():
	"""All the informations concerning the crypto we want to look at"""
	def __init__(self, id, name, ticker, price, date_price, logo, circulating_supply, rank):
		super(Cryptocurrency, self).__init__(name, id)
		self.ticker = ticker



	def get_price_change(self, delay):
		""" function to get the evolution of the price between 2 dates: like one week, one day """
		pass


	def get_price_change_year(self):
		""" get the evolution of the price on 1 year """
		pass

	def update_data(self):
		""" the new data from the api is gonna be updated in the arguments """
		pass

