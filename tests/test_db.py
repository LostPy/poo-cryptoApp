import os.path
import sys
sys.path.append(os.path.abspath("../poo-crypto-common"))
print(sys.path)

from crypto_common.db import CryptoDatabase

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
    'portofolio_id': None
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
portofolio_id = db.insert_portofolio(PORTOFOLIO)
TRANSACTION['portofolio_id'] = portofolio_id
db.insert_transaction(TRANSACTION)
print("data inserted")

# Select
# ----------

currency_by_id = db.get_currency_by_id("bitcoin")
currency_by_name = db.get_currency_by_name("Bitcoin")
currency_by_name2 = db.get_currencies_contains_name("coin")
print(currency_by_id)
print(currency_by_name)
print(currency_by_name2)

portofolio_by_id = db.get_portofolio_by_id(1)
portofolio_by_name = db.get_portofolio_by_name("test")
print(portofolio_by_id)
print(portofolio_by_name)

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

# Update
# ----------

currency_update = {'id': 'bitcoin', 'logo': "/path/logo/bitcoin"}
db.update_currency(currency_update)
currency_by_id = db.get_currency_by_id("bitcoin")

if currency_by_id['logo'] == currency_update['logo']:
    print('currency update: Ok')
else:
    print('currency update: Error\n', currency_by_id)

portofolio_update = {'id': 1, 'name': 'test', 'password': 'password456'}
db.update_portofolio(portofolio_update)
portofolio_by_id = db.get_portofolio_by_id(1)
print(portofolio_by_id)

transaction_update = TRANSACTION | {'id': 1, 'currency_send_id': 'euro'}
transaction_update.pop('portofolio_id')
db.update_transaction(transaction_update)
transaction_by_id = db.get_transaction_by_id(1)
print(transaction_by_id)

# Delete
# ----------
db.delete_currencies(['bitcoin'])
db.delete_transactions([1])
db.delete_portofolio(1)

currency_by_id = db.get_currency_by_id("bitcoin")
transaction_by_id = db.get_transaction_by_id(1)
portofolio_by_id = db.get_portofolio_by_id(1)
print(currency_by_id)
print(transaction_by_id)
print(portofolio_by_id)

# Remove database
db.close()
db.remove()
