import sys
sys.PATH.append("..")

from crypto_common.db import CryptoDatabase


db = CryptoDatabase(CryptoDatabase.create_connection("test"))
db.init_database(remove_existing=True)
