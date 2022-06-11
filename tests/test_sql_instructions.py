import os.path
import sys
sys.path.append(os.path.abspath("../poo-crypto-common/cryptoApp"))
print(sys.path)

from crypto_core.db.sql_instructions import *


print(create_table("User", ["idUser", "name", "password"]))
print(insert("User", ["idUser", "name", "password"], [0, "username", "some password"]))
print(where({"idUser": ("=", 0)}))
print(order_by("name"))
print(update("User", {"name": "new name"}, where=where({"idUser": ("=", 0)})))
print(select("User", ["idUser", "name"], where=where({"idUser": ("=", 0)}), order_by=order_by("name")))

print(create_table(
    "CryptoTransaction",
    [
        "idTransaction integer PRIMARY KEY",
        "date timestamp",
        "amountSend real",
        "amountReceived real",
        "currencySend integer NOT NULL",
        "currencyReceived integer NOT NULL",
        "portfolio integer NOT NULL",
        "FOREIGN KEY (currencySend) REFERENCES Currency(idCurrency)",
        "FOREIGN KEY (currencyReceived) REFERENCES Currency(idCurrency)",
        "FOREIGN KEY (portfolio) REFERENCES Portfolio(idPortfolio)"
    ]
))
