import os.path
import sys
sys.path.append(os.path.abspath("../poo-crypto-common"))
print(sys.path)

from crypto_common.db import CryptoDatabase


db = CryptoDatabase(CryptoDatabase.create_connection("test"))
db.init_database(remove_existing=True)
