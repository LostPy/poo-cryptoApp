import os.path
import sys
sys.path.append(os.path.abspath("../poo-crypto-common/cryptoApp"))
print(sys.path)


from crypto_core.objects import Portofolio
from crypto_core.db import CryptoDatabase
from utils.hashstring import hash_string


database = CryptoDatabase.create_connection()
database.init_database(remove_existing=True)
database.open()


def test_Portofolio():
    portofolio = Portofolio.new_portofolio(
        "test", hash_string("mypassword123"), database)
    print(portofolio)
    print(portofolio.password)

    # to check if a password correspond to the portofolio password:
    test1 = "mypassword123"
    test2 = "otherpassword"
    result1 = portofolio.password == hash_string(test1)
    result2 = portofolio.password == hash_string(test2)
    print(f"login successful with '{test1}': ", result1)
    print(f"login successful with '{test2}': ", result2)

    # insert a second portofolio
    portofolio2 = Portofolio.new_portofolio(
        "second portofolio", hash_string('otherpassword'), database)
    print(portofolio2)

    # test get the portofolio list
    portofolios = Portofolio.get_all_portofolios(database)
    print(portofolios)


test_Portofolio()
database.remove()
