import sys
sys.PATH.append("..")

from crypto_common.db.sql_instructions import *


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
        "portofolio integer NOT NULL",
        "FOREIGN KEY (currencySend) REFERENCES Currency(idCurrency)",
        "FOREIGN KEY (currencyReceived) REFERENCES Currency(idCurrency)",
        "FOREIGN KEY (portofolio) REFERENCES Portofolio(idPortofolio)"
    ]
))
