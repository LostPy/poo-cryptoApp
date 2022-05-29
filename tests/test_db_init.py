import os.path
import sys
sys.path.append(os.path.abspath("../poo-crypto-common/cryptoApp"))
print(sys.path)

from crypto_core.db import CryptoDatabase


db = CryptoDatabase(CryptoDatabase.create_connection())
db.init_database(remove_existing=True)
