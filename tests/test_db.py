
import os.path
import sys
sys.path.append(os.path.abspath("../poo-crypto-common/cryptoApp"))
print(sys.path)

from datetime import datetime
from crypto_core.db import CryptoDatabase

from datetime import datetime


##################
### Test Setup ###
##################

CURRENCIES = [
    {
        'id': 'bitcoin',
        'name': "Bitcoin",
        'ticker': "btc",
        'price': 26935,
        'logo': None,
        'circulating_supply': 120954445,
        'last_update': datetime.now(),
        'rank': 1,
        'is_crypto': True
    },

    {
        'id': 'ethereum',
        'name': 'Ethereum',
        'ticker': 'eth',
        'price': 1644.18,
        'logo': "/path/logo",
        'circulating_supply': 53557474665,
        'last_update': datetime.now(),
        'rank': 2,
        'is_crypto': True
    }
]


PORTOFOLIO = {
    'name': 'test',
    'password': 'password1234'
}

TRANSACTION = {
    'date': datetime.now(),
    'amount_send': 10.5,
    'amount_received': 2,
    'currency_send_id': 'dollar',
    'currency_received_id': 'bitcoin',
    'portfolio_id': None
}

CryptoDatabase.init_database(remove_existing=True)
print("database initialized")

############
### Test ###
############

db = CryptoDatabase.create_connection()

# Insertion
# ----------

db.insert_currencies(CURRENCIES, commit=False)
portfolio_id = db.insert_portfolio(PORTOFOLIO)
TRANSACTION['portfolio_id'] = portfolio_id
db.insert_transaction(TRANSACTION)
db.insert_currency_portfolio(portfolio_id, "bitcoin", 100)
print("data inserted")

# Select
# ----------

currency_by_id = db.get_currency_by_id("bitcoin")
currency_by_name = db.get_currency_by_name("Bitcoin")
print(currency_by_id)
print(currency_by_name)

portfolio_by_id = db.get_portfolio_by_id(1)
print(portfolio_by_id)

transaction_by_id = db.get_transaction_by_id(1)
transactions_filtered = db.get_transactions_filter(
    1,
    currency_send_id="dollar",
    range_amount_send=(None, 20))
transactions_filtered_2 = db.get_transactions_filter(
    1,
    currency_send_id='dollar',
    range_amount_received=(1000, 2000))
print(transaction_by_id)
print(transactions_filtered)
print(transactions_filtered_2)


currency_portfolio = db.get_currencies_portfolios(1)
print(currency_portfolio)


# Update
# ----------

currency_update = {'id': 'bitcoin', 'last_update': datetime(2022, 6, 1)}
db.update_currency(currency_update)
currency_by_id = db.get_currency_by_id("bitcoin")

if currency_by_id['last_update'] == currency_update['last_update']:
    print('currency update: Ok')
else:
    print('currency update: Error\n', currency_by_id['last_update'], '!=', currency_update['last_update'])

portfolio_update = {'id': 1, 'name': 'test', 'password': 'password456'}
db.update_portfolio(portfolio_update)
portfolio_by_id = db.get_portfolio_by_id(1)
print(portfolio_by_id)

transaction_update = TRANSACTION | {'id': 1, 'currency_send_id': 'euro'}
transaction_update.pop('portfolio_id')
db.update_transaction(transaction_update)
transaction_by_id = db.get_transaction_by_id(1)
print(transaction_by_id)

db.update_currency_portfolio(1, 'bitcoin', 20)
print(db.get_currencies_portfolios(1))

# Delete
# ----------
db.delete_currencies(['bitcoin'])
db.delete_transactions([1])
db.delete_currency_portfolio(1, 'bitcoin')
db.delete_portfolio(1)

currency_by_id = db.get_currency_by_id("bitcoin")
transaction_by_id = db.get_transaction_by_id(1)
portfolio_by_id = db.get_portfolio_by_id(1)
print(currency_by_id)
print(transaction_by_id)
print(portfolio_by_id)
print(db.get_currencies_portfolios(1))

# Remove database
db.close()
db.remove()
