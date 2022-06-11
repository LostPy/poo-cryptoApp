import os.path
import sys
sys.path.append(os.path.abspath("../poo-crypto-common/"))
sys.path.append(os.path.abspath("../poo-crypto-common/cryptoApp/"))
print(sys.path)


from PySide6.QtWidgets import QApplication
from cryptoApp.crypto_core.objects import Portfolio, Currency, Cryptocurrency
from cryptoApp.crypto_ui.widgets import PortfolioChart

app = QApplication(sys.argv)
portfolio = Portfolio(0, "Test", "")
portfolio.currencies[Cryptocurrency('bitcoin', "Bitcoin", 'btc', price=40000, circulating_supply=10000000, rank=1)] = 0.3
portfolio.currencies[Cryptocurrency('ethereum', "Ethereum", 'eth', price=2000, circulating_supply=10000000, rank=2)] = 10 
w = PortfolioChart()
w.set_portfolio(portfolio)
w.show()
app.exec()

