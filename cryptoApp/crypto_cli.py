"""An alternative to the GUI
"""
from logging import ERROR
from datetime import datetime
import click
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate

from crypto_core.db import CryptoDatabase
from crypto_core.objects import Portofolio, Currency, Cryptocurrency, Transaction
from crypto_core import crypto_api, errors
from utils.hashstring import hash_string


######################
### Initialisation ###
######################
CryptoDatabase.LOGGER.setLevel(ERROR)

if not CryptoDatabase.PATH.exists():
    CryptoDatabase.init_database()
    database = CryptoDatabase.create_connection()
    Currency.init_currencies(database)
    # Add a base of cryptocurrencies in database
    Cryptocurrency.get_top_coins_market(Currency.CURRENCIES['euro'], database=database)
    database.close()
    del database

if not Cryptocurrency.LOGO_DIR_PATH.exists():
    Cryptocurrency.LOGO_DIR_PATH.mkdir()

database = CryptoDatabase.create_connection()
if len(Currency.CURRENCIES) == 0:
    Currency.init_currencies(database)
if len(Cryptocurrency.CRYPTOCURRENCIES) == 0:
    Cryptocurrency.init_cryptocurrencies(database)

portfolios = Portofolio.get_all_portofolios(database)
names_portfolio = [portfolio.name for portfolio in portfolios]
print(Currency.CURRENCIES)
print(Cryptocurrency.CRYPTOCURRENCIES)

##################################
### Functions utils use in cli ###
##################################
def custom_pct(pct, allvals):
    """Function to create text label in a pie plot.\
    This function must be passed to the `plt.pie` function.
    """
    absolute = int(pct / 100. * sum(allvals))
    return f"{pct:.1f}%\n({absolute:d})"


def parse_currency_id(currency_id) -> Currency:
    """Returns a Currency from the id.
    If this id does not exist in dictionary `Currency.CURRENCIES` or \
    `Cryptocurrency.CRYPTOCURRENCIES`, try to get currency from the database. \
    If currency does not exist in database, try to get currency from API. \
    If currency is not found in API, returns None.

    Parameters
    ----------
    currency_id : str
        The currency id

    Returns
    -------
    Currency
        The currency corresponding to the id
    """
    if currency_id in Cryptocurrency.CRYPTOCURRENCIES.keys():
        return Cryptocurrency.CRYPTOCURRENCIES[currency_id]
    elif currency_id in Currency.CURRENCIES.keys():
        return Currency.CURRENCIES[currency_id]
    else:
        try:
            return Cryptocurrency.from_db(currency_id, database)
        except errors.CurrencyDbNotFound:
            try:
                return Cryptocurrency.from_api(
                    currency_id, Currency.CURRENCIES['euro'].gecko_id, database=database)
            except Exception as e:  # TODO: replace Exception by a custom specific API exception (ConnectionError and id inexisting)
                print('api error: ', str(e))
                return None


###########
### CLI ###
###########
@click.group()
def cli():
    """Interface to create a portfolio, login to a portfolio or get various data on cryptocurrencies.
    """
    pass


@click.command(name='new-portfolio')
@click.argument('name', nargs=1, type=click.STRING)
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True)
def new_portfolio(name: str, password: str):
    """Create a new portfolio in the database.
    """
    Portofolio.new_portofolio(name, hash_string(password), database)
    click.echo(
        click.style("The portfolio ", fg='green')
        + click.style(name, bold=True)
        + click.style(" is created with success", fg='green'))
    database.close()


@click.command()
@click.option('--portfolio',
              prompt="The portfolio's name please",
              type=click.Choice(names_portfolio))
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=False)
def login(portfolio, password):
    """Login to a portfolio and open an interactive mode.
    """
    portfolio = portfolios[names_portfolio.index(portfolio)]
    if not portfolio.password == hash_string(password):
        click.echo(click.style(
                       f"The password don't correspond to the portfolio '{portfolio.name}'",
                       fg='red'),
                   err=True)
        return

    click.echo(
        click.style("login with success to the portfolio ", fg='green')
        + click.style(portfolio.name, bold=True))

    portfolio.load_currencies(database)  # load registered currencies of portfolio

    click.clear()  # clear the screen
    click.echo(f"\n\n{'=' * 20}\n{' ' * 8}Menu\n{'=' * 20}\n")

    quit = False
    while not quit:
        click.echo("""Select an action:
        1- Add a transaction
        2- Display transactions
        3- Display currencies
        4- Display currencies pie chart
        5- Quit
        """)
        choice = int(click.prompt("Your choice", type=click.Choice([str(i) for i in range(1, 6)])))

        if choice == 1:  # Add a transaction
            # User input
            # ----------
            currency_id_send = click.prompt(
                "The currency id spend (no cryptocurrency avaible: "
                f"{', '.join(list(Currency.CURRENCIES.keys()))})",
                type=click.STRING
            ).lower()
            amount_send = click.prompt("The amount spend (a float)", type=click.FLOAT)
            currency_id_received = click.prompt(
                "The currency id bought (no cryptocurrency avaible: "
                f"{', '.join(list(Currency.CURRENCIES.keys()))})",
                type=click.STRING
            ).lower()
            amount_received = click.prompt("The amount bought (a float)", type=click.FLOAT)

            # Parse data
            # ----------
            try:
                currency_send = parse_currency_id(currency_id_send)
                currency_received = parse_currency_id(currency_id_received)
            except:  # Add exception for API connection error
                click.echo(click.style(
                               "This currency doesn't exist in database and "
                               "connection to the API failed: check your connection.",
                               fg='red'),
                           err=True)
                click.pause("Press a key to continue...")
                click.clear()  # clear the screen
                continue  # skip the next instruction and go to next iteration

            if currency_send is not None and currency_received is not None:
                click.echo("The following transaction will be added:")
                click.echo(f"\t- spend: {amount_send} {currency_send.ticker}")
                click.echo(f"\t- bought: {amount_received} {currency_received.ticker}")
                if click.confirm("Do want to continue ?"):
                    portfolio.add_transaction(
                        send=(currency_send, amount_send),
                        received=(currency_received, amount_received),
                        database=database
                    )
                    click.echo("The transaction was added!")
                else:
                    click.echo("The transaction was cancelled.")

            elif currency_send is None and currency_received is None:
                click.echo(click.style(
                   "These currencies don't exist in database and in CoinGeckoAPI.",
                   fg='red'
                ))

            elif currency_send is None:
                click.echo(click.style(
                   "The currency spend doesn't exist in database and in CoinGeckoAPI",
                   fg='red'
                ))

            elif currency_received is None:
                click.echo(click.style(
                   "The currency bought doesn't exist in database and in CoinGeckoAPI",
                   fg='red'
                ))


            click.pause("Press a key to continue...")

        elif choice == 2:  # Display transactions
            start = click.prompt(
                "The date of the oldest transaction to be displayed",
                type=click.DateTime(), default=datetime(2010, 1, 1))
            end = click.prompt(
                "The date of the most recent transaction to be displayed",
                type=click.DateTime(), default=datetime(2100, 1, 1))
            transactions = [
                (
                    transaction.id,
                    transaction.date,
                    transaction.currency_send,
                    transaction.amount_send,
                    transaction.currency_received,
                    transaction.amount_received
                )
                for transaction in portfolio.get_transactions(database, start, end)
            ]
            headers = (
                'Id',
                'Datetime',
                'Currency spend',
                'Amount spend',
                'Currency bought',
                'Amount bought'
            )
            print(tabulate(transactions, headers, tablefmt='rst'))
            click.pause("Press a key to continue...")

        elif choice == 3 and len(portfolio.currencies) > 0:  # Display currencies
            for currency, amount in sorted(portfolio.currencies.items(),
                                           key=lambda item: item[1]):
                print(f"{currency.name}: {amount}{currency.ticker.upper()}")
            click.pause("Press a key to continue...")

        # Display cryptocurrencies in pie chart
        elif choice == 4 and len(portfolio.cryptocurrencies) > 0:
            labels = list()
            values = list()
            for currency, amount in portfolio.cryptocurrencies.items():
                labels.append(f"{currency.name} ({currency.ticker.upper()})")
                values.append(amount * currency.price)
            plt.pie(values,
                    labels=labels,
                    autopct=lambda pct: custom_pct(pct, values),
                    textprops=dict(color='w'))
            plt.title(f"Registered cryptocurrencies of {portfolio.name}")
            plt.legend()
            plt.show()

        # Display currencies but there is not registered currencies
        elif choice in (3, 4):
            click.echo("You don't have registered currencies.")
            click.pause("Press a key to continue...")

        # Quit
        elif choice == 5:
            quit = True
        click.clear()  # clear the screen

    portfolio.upload_currencies_in_db(database)
    database.close()


@click.command(name="market-chart")
@click.argument('cryptos', type=str, nargs=-1)
@click.option('-d', '--days', type=click.IntRange(min=1, max=30, clamp=True), default=30)
@click.option('--currency', type=click.Choice(['usd', 'eur']), default='usd')
def market_chart(cryptos, days, currency):
    """Display market chart of a cryptocurrency in a line plot."""
    data = {
        crypto: crypto_api.get_market_chart(crypto.lower(), currency, days)
        for crypto in cryptos
    }
    currency_symbol = '€' if currency in ('eur') else '$'
    fig = plt.figure(figsize=(10, 4 * len(cryptos)))
    fig.subplots_adjust(
        hspace=0.1 * len(cryptos) + 0.1,  # setup space betwwen subplot
        top=0.9,
        bottom=0.1
    )
    for i, (crypto, df) in enumerate(data.items()):
        df['date'] = pd.to_datetime(df['date'], unit='ms')
        plt.subplot(len(cryptos), 1, i + 1)
        plt.plot(df['date'], df['price'], label=crypto.capitalize())
        plt.xticks(rotation=20)
        plt.grid()
        plt.title(f"Market chart for {crypto} in {currency_symbol}")
    plt.show()
    database.close()


cli.add_command(new_portfolio)
cli.add_command(login)
cli.add_command(market_chart)


if __name__ == '__main__':
    cli()
