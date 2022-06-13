import os.path
import sys
sys.path.append(os.path.abspath("../poo-crypto-common/cryptoApp"))
print(sys.path)


from crypto_core.objects import Portfolio
from crypto_core.db import CryptoDatabase
from utils.hashstring import hash_string


database = CryptoDatabase.create_connection()
database.init_database(remove_existing=True)
database.open()


def test_Portfolio():
    portfolio = Portfolio.new_portfolio(
        "test", hash_string("mypassword123"), database)
    print(portfolio)
    print(portfolio.password)

    # to check if a password correspond to the portfolio password:
    test1 = "mypassword123"
    test2 = "otherpassword"
    result1 = portfolio.password == hash_string(test1)
    result2 = portfolio.password == hash_string(test2)
    print(f"login successful with '{test1}': ", result1)
    print(f"login successful with '{test2}': ", result2)

    # insert a second portfolio
    portfolio2 = Portfolio.new_portfolio(
        "second portfolio", hash_string('otherpassword'), database)
    print(portfolio2)

    # test get the portfolio list
    portfolios = Portfolio.get_all_portfolios(database)
    print(portfolios)


test_Portfolio()
database.remove()
