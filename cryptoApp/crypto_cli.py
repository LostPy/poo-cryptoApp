"""An alternative to the GUI
"""
import click
import pandas as pd
import matplotlib.pyplot as plt

from crypto_core.db import CryptoDatabase
from crypto_core.objects import Portofolio
from crypto_core import crypto_api
from utils.hashstring import hash_string


def custom_pct(pct, allvals):
    """Function to create text label in a pie plot.\
    This function must be passed to the `plt.pie` function.
    """
    absolute = int(pct / 100. * sum(allvals))
    return f"{pct:.1f}%\n({absolute:d})"


if not CryptoDatabase.PATH.exists():
    CryptoDatabase.init_database()

database = CryptoDatabase.create_connection()
portfolios = Portofolio.get_all_portofolios(database)
names_portfolio = [portfolio.name for portfolio in portfolios]


@click.group()
def cli():
    """Interface to create a portfolio, login to a portfolio or get various data on cryptocurrencies.
    """
    pass


@click.command(name='new-portfolio')
@click.argument('name', nargs=1, type=str)
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True)
def new_portfolio(name: str, password: str):
    """Create a new portfolio in the database.
    """
    Portofolio.new_portofolio(name, hash_string(password), database)
    click.echo(
        click.style("The portfolio ", fg='green')
        + click.style(name, bold=True)
        + click.style(" is created with success", fg='green'))


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

    click.clear()
    click.echo(f"\n\n{'=' * 20}\n{' ' * 8}Menu\n{'=' * 20}\n")

    quit = False
    while not quit:
        click.echo("""Select an action:
        1- Add a transaction
        2- Display transactions
        3- Remove a transaction
        4- Display currencies
        5- Display currencies pie chart
        6- Quit
        """)
        choice = int(click.prompt("Your choice", type=click.Choice([str(i) for i in range(1, 7)])))

        if choice == 1:
            click.pause("Press a key to continue...")

        elif choice == 2:
            click.pause("Press a key to continue...")

        elif choice == 3:
            click.pause("Press a key to continue...")

        elif choice == 4 and len(portfolio.currencies) > 0:
            for currency, amount in sorted(portfolio.currencies.items(),
                                           key=lambda item: item[1]):
                print(f"{currency.name}: {amount}{currency.ticker.upper()}")
            click.pause("Press a key to continue...")

        elif choice == 5 and len(portfolio.currencies) > 0:
            labels = list()
            values = list()
            for currency, amount in portfolio.currencies:
                labels.append(f"{currency.name} ({currency.ticker.upper()})")
                values.append(amount * currency.price)
            plt.pie(values,
                    autopct=lambda pct: custom_pct(pct, values),
                    textprops=dict(color='w'))
            plt.legend()
            plt.title(f"Registered cryptocurrencies of {portfolio.name}")
            plt.show()

        elif choice in (4, 5):
            click.echo("You don't have registered currencies.")
            click.pause("Press a key to continue...")

        elif choice == 6:
            quit = True
        click.clear()  # clear the screen


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
    currency_symbol = '€' if currency == 'eur' else '$'
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


cli.add_command(new_portfolio)
cli.add_command(login)
cli.add_command(market_chart)


if __name__ == '__main__':
    cli()
