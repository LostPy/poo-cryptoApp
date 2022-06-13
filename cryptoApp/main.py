"""Main file for CryptoApp, it's the entry point.
"""
import sys
import logging

from PySide6.QtWidgets import QApplication


from crypto_core.db import CryptoDatabase
from crypto_core.objects import Portfolio, Currency, Cryptocurrency
from utils import new_logger
from crypto_ui import MainWindowCrypto



main_logger = new_logger("MAIN", level=logging.DEBUG)

# Initialisation de l'application
# -------------------------------
CryptoDatabase.LOGGER.setLevel(logging.DEBUG)

if not CryptoDatabase.PATH.exists():
    CryptoDatabase.init_database()
    database = CryptoDatabase.create_connection()
    Currency.init_currencies(database)
    # Add a base of cryptocurrencies in database
    Cryptocurrency.get_top_coins_market(Currency.CURRENCIES['euro'], database=database)
    database.close()
    del database

database = CryptoDatabase.create_connection()
if len(Currency.CURRENCIES) == 0:
    Currency.init_currencies(database)
if len(Cryptocurrency.CRYPTOCURRENCIES) == 0:
    Cryptocurrency.init_cryptocurrencies(database)
database.close()
del database

# Initialisation de l'interface
# -----------------------------
main_logger.info("Initialisation of the application...")
app = QApplication(sys.argv)
w = MainWindowCrypto()
w.show()
result = app.exec()

if result == 0:
    main_logger.info("Application interrupted whith success")
else:
    main_logger.warning(f"Application interrupted on a error: {result}")
sys.exit(result)
