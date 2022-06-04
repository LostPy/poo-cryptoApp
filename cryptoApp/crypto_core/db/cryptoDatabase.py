from typing import Union
from pathlib import Path
from datetime import datetime
import sqlite3
import __main__  # to get the path of __main__ (Python file executed)

from PySide6.QtCore import QFile, QIODevice

from ressources import scripts_rc
from utils import new_logger

from .. import errors
from .sql_instructions import (
    create_table,
    insert,
    select,
    update,
    delete,
    where
)


def _dict_factory(cursor, row):
    """Parse a row from a sql query in a dictionary."""
    return {col[0]: row[index] for index, col in enumerate(cursor.description)}


class CryptoDatabase:
    """Class to work with the 'crypto.db' sqlite database.
    """

    LOGGER = new_logger("DATABASE")

    # The database is in the "root" of project
    PATH: Path = Path(__main__.__file__).parent / 'crypto.db'

    # Currency to init
    # TODO: Change this tuple in Currency object
    BASE_CURRENCIES = [
        ('dollar', "Dollar", "usd", 0),
        ('euro', "Euro", "eur", 0)
    ]

    def __init__(self, connection: sqlite3.Connection):
        self.connection: sqlite3.Connection = connection

    def get_currencies(self,
                       where: str = "",
                       where_args: tuple = None,
                       fetchone: bool = False) -> Union[dict, list[dict]]:
        cursor = self.connection.cursor()
        sql_instruction = select(
            "Currency",
            where=where,
            columns=[
                "idCurrency",
                "name",
                "ticker",
                "price",
                "circulatingSupply",
                "last_update",
                "rank",
                "isCrypto"
            ]
        )

        if where_args is None:
            cursor.execute(sql_instruction)
        else:
            cursor.execute(sql_instruction, where_args)

        if fetchone:
            return cursor.fetchone()
        return cursor.fetchall()

    def get_portofolios(self,
                        where: str = "",
                        where_args: tuple = None,
                        fetchone: bool = False) -> Union[dict, list[dict]]:
        cursor = self.connection.cursor()
        sql_instruction = select(
            "Portofolio",
            columns=[
                "idPortofolio",
                "name",
                "password"
            ],
            where=where
        )
        if where_args is None:
            cursor.execute(sql_instruction)
        else:
            cursor.execute(sql_instruction, where_args)

        if fetchone:
            return cursor.fetchone()
        return cursor.fetchall()

    def get_currencies_portofolios(self,
                                   portofolio_id: int) -> list[dict]:
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT idCurrency, name, ticker, price, circulatingSupply,
            last_update, rank, isCrypto, amount
            FROM PortofoliosCurrencies
            INNER JOIN Currency ON PortofoliosCurrencies.currency = Currency.idCurrency
            WHERE portofolio=?
            """,
            (portofolio_id, ))
        return cursor.fetchall()

    def get_transactions(self,
                         where: str = "",
                         where_args: tuple = None,
                         fetchone: bool = False) -> Union[dict, list[dict]]:
        cursor = self.connection.cursor()
        sql_instruction = select(
            "CryptoTransaction",
            columns=[
                "idTransaction",
                "date",
                "amountSend",
                "amountReceived",
                "currencySend",
                "currencyReceived",
            ],
            where=where
        )
        if where_args is None:
            cursor.execute(sql_instruction)
        else:
            cursor.execute(sql_instruction, where_args)

        if fetchone:
            return cursor.fetchone()
        return cursor.fetchall()

    def get_currency_by_id(self, id_: int, crypto: Union[bool, int] = 1) -> dict:
        return self.get_currencies(
            where=where({
                "idCurrency": ("=", id_),
                "isCrypto": ('=', int(crypto))}),
            fetchone=True
        )

    def get_currency_by_name(self, name: str, crypto: Union[bool, int] = 1) -> dict:
        return self.get_currencies(
            where=where({
                "name": ("=", name.capitalize()),
                "isCrypto": ('=', int(crypto))}),
            fetchone=True
        )

    def get_currencies_contains_name(self,
                                     name: str,
                                     crypto: Union[bool, int] = 1) -> list[dict]:
        return self.get_currencies(
            where=where({
                "name": ("LIKE", f"%{name.lower()}%"),
                "isCrypto": ('=', int(crypto))
            })
        )

    def get_portofolio_by_id(self, id_: int) -> dict:
        return self.get_portofolios(
            where=where({"idPortofolio": ("=", id_)}), fetchone=True)

    def get_portofolio_by_name(self, name: str) -> dict:
        return self.get_portofolios(
            where=where({"name": ('=', name)}), fetchone=True)

    def get_transaction_by_id(self, id_: int) -> dict:
        return self.get_transactions(
            where=where({"idTransaction": ('=', id_)}), fetchone=True)

    def get_top_cryptocurrencies(self, rank_max: int = 5) -> list[dict]:
        return self.get_currencies(
            where=where({"rank": ('<=', rank_max), "isCrypto": ('=', 1)}))

    def get_transactions_filter(self, portofolio_id: int, /,
                                currency_send_id: int = None,
                                currency_receive_id: int = None,
                                range_amount_send: tuple[float, float] = None,
                                range_amount_received: tuple[float, float] = None,
                                range_date: tuple[datetime, datetime] = None) -> list[dict]:
        filter_ = dict(portofolio=("=", portofolio_id))

        if currency_send_id is not None:
            filter_['currencySend'] = ('=', currency_send_id)

        if currency_receive_id is not None:
            filter_['currencyReceived'] = ('=', currency_send_id)

        if range_amount_send is not None:

            if range_amount_send[0] is not None and\
                    range_amount_send[1] is not None:
                filter_['amountSend'] = (
                    'BETWEEN ? AND ?', list(range_amount_send))

            elif range_amount_send[0] is not None:
                filter_['amountSend'] = ('>=', range_amount_send[0])

            elif range_amount_send[1] is not None:
                filter_['amountSend'] = ('<=', range_amount_send[1])

        if range_amount_received is not None:
            if range_amount_received[0] is not None\
                    and range_amount_received[1] is not None:
                filter_['amountReceived'] = (
                    'BETWEEN ? AND ?', list(range_amount_received))

            elif range_amount_received[0] is not None:
                filter_['amountReceived'] = ('>=', range_amount_received[0])

            elif range_amount_received[1] is not None:
                filter_['amountReceived'] = ('<=', range_amount_received[1])

        if range_date is not None:
            if range_date[0] is not None and range_date[1] is not None:
                filter_['date'] = ('BETWEEN ? AND ?', list(range_date))

            elif range_date[0] is not None:
                filter_['date'] = ('>=', range_date[0])

            elif range_date[1] is not None:
                filter_['date'] = ('<=', range_date[1])

        where = "WHERE "
        where_args = list()
        for k, v in filter_.items():
            if isinstance(v[1], list):
                where += f"{k} {v[0]}"
                where_args += v[1]
            else:
                where += f"{k} {v[0]} ? AND "
                where_args.append(v[1])

        if where.endswith(" AND "):
            where = where[:-5]  # remove last " AND "

        return self.get_transactions(where=where, where_args=where_args)

    def insert_currencies(self,
                          currencies: Union[dict, list[dict]],
                          ignore: bool = False,
                          commit: bool = True) -> int:

        sql_instruction = insert(
            "Currency",
            [
                'idCurrency',
                'name',
                'ticker',
                'price',
                'circulatingSupply',
                'last_update',
                'rank',
                'isCrypto'
            ],
            ignore=ignore
        )

        if isinstance(currencies, dict):
            try:
                values = (
                    currencies['id'],
                    currencies['name'],
                    currencies.get('ticker'),
                    currencies.get('price'),
                    currencies.get('circulating_supply'),
                    currencies.get('last_update'),
                    currencies.get('rank'),
                    currencies.get('is_crypto')
                )
            except KeyError as e:
                raise errors.DbRequestMissingData(e.args[0])
            cursor = self.connection.cursor()
            cursor.execute(sql_instruction, values)

        elif isinstance(currencies, list) and isinstance(currencies[0], dict):
            try:
                values = [(
                    currency['id'],
                    currency['name'],
                    currency.get('ticker'),
                    currency.get('price'),
                    currency.get('circulating_supply'),
                    currency.get('last_update'),
                    currency.get('rank'),
                    currency.get('is_crypto')
                )
                    for currency in currencies
                ]
            except KeyError as e:
                raise errors.DbRequestMissingData(e.args[0])
            cursor = self.connection.cursor()
            cursor.executemany(sql_instruction, values)

        else:
            raise ValueError(
                "'currencies' must be a dictionary or a list "
                f" of dictionaries, not an instance of '{type(currencies)}'."
            )

        if commit:
            self.connection.commit()

    def insert_portofolio(self, portofolio: dict, commit: bool = True):
        sql_instruction = insert(
            'Portofolio',
            [
                'name',
                'password'
            ]
        )

        try:
            values = (
                portofolio['name'],
                portofolio['password']
            )
        except KeyError as e:
            raise errors.DbRequestMissingData(e.args[0])

        cursor = self.connection.cursor()
        cursor.execute(sql_instruction, values)
        id_ = cursor.lastrowid

        if commit:
            self.connection.commit()

        return id_

    def insert_currency_portofolio(self,
                                   portofolio_id: int,
                                   currency_id: str,
                                   amount: float,
                                   commit: bool = True):
        sql_instruction = insert(
            "PortofoliosCurrencies",
            ['portofolio', 'currency', 'amount'])

        cursor = self.connection.cursor()
        cursor.execute(sql_instruction, (portofolio_id, currency_id, amount))

        if commit:
            self.connection.commit()

    def insert_transaction(self, transaction: dict, commit: bool = True):
        sql_instruction = insert(
            'CryptoTransaction',
            [
                'date',
                'amountSend',
                'amountReceived',
                'currencySend',
                'currencyReceived',
                'portofolio'
            ]
        )

        try:
            values = (
                transaction['date'],
                transaction['amount_send'],
                transaction['amount_received'],
                transaction['currency_send_id'],
                transaction['currency_received_id'],
                transaction['portofolio_id']
            )
        except KeyError as e:
            raise errors.DbRequestMissingData(e.args[0])

        cursor = self.connection.cursor()
        cursor.execute(sql_instruction, values)
        id_ = cursor.lastrowid

        if commit:
            self.connection.commit()

        return id_

    def update_currency(self, currency: dict, commit: bool = True):
        columns = ['price', 'circulatingSupply', 'last_update', 'rank']
        values = list()
        nb_col_delete = 0
        for i, attr_name in enumerate(['price', 'circulating_supply', 'last_update', 'rank']):
            if currency.get(attr_name) is None:
                columns.pop(i - nb_col_delete)
                nb_col_delete += 1
            else:
                values.append(currency[attr_name])

        try:
            values.append(currency['id'])  # for WHERE statement
        except KeyError:
            raise errors.DbRequestMissingData("id")

        cursor = self.connection.cursor()
        cursor.execute(
            update('Currency', columns, where="WHERE idCurrency=?"),
            tuple(values)
        )

        if commit:
            self.connection.commit()

    def update_portofolio(self, portofolio: dict, commit: bool = True):
        sql_instruction = update(
            'Portofolio',
            [
                'name',
                'password'
            ],
            where="WHERE idPortofolio=?"
        )

        try:
            values = (
                portofolio['name'],
                portofolio['password'],
                portofolio['id']
            )
        except KeyError as e:
            raise errors.DbRequestMissingData(e.args[0])

        cursor = self.connection.cursor()
        cursor.execute(sql_instruction, values)

        if commit:
            self.connection.commit()

    def update_currency_portofolio(self,
                                   portofolio_id: int,
                                   currency_id: str,
                                   amount: float,
                                   commit: bool = True):
        sql_instruction = update(
            "PortofoliosCurrencies",
            ['amount'],
            where="WHERE portofolio=? AND currency=?")

        cursor = self.connection.cursor()
        cursor.execute(sql_instruction, (amount, portofolio_id, currency_id))

        if commit:
            self.connection.commit()

    def update_transaction(self, transaction: dict, commit: bool = True):
        sql_instruction = update(
            'CryptoTransaction',
            [
                'date',
                'amountSend',
                'amountReceived',
                'currencySend',
                'currencyReceived',
            ],
            where="WHERE idTransaction=?"
        )

        try:
            values = (
                transaction['date'],
                transaction['amount_send'],
                transaction['amount_received'],
                transaction['currency_send_id'],
                transaction['currency_received_id'],
                transaction['id']
            )
        except KeyError as e:
            raise errors.DbRequestMissingData(e.args[0])

        cursor = self.connection.cursor()
        cursor.execute(sql_instruction, values)

        if commit:
            self.connection.commit()

    def delete_currencies(self, ids: list[str], commit: bool = True):
        cursor = self.connection.cursor()
        values = [(id_, ) for id_ in ids]
        cursor.executemany(delete('Currency', "WHERE idCurrency=?"), values)
        if commit:
            self.connection.commit()

    def delete_portofolio(self, id_: int, commit: bool = True):
        cursor = self.connection.cursor()
        cursor.execute(delete('Portofolio', "WHERE idPortofolio=?"), (id_, ))
        cursor.execute(delete('PortofoliosCurrencies', "WHERE portofolio=?"), (id_, ))
        cursor.execute(delete('CryptoTransaction', "WHERE portofolio=?"), (id_, ))
        if commit:
            self.connection.commit()

    def delete_currency_portofolio(self,
                                   portofolio_id: int,
                                   currency_id: str,
                                   commit: bool = True):
        sql_instruction = delete(
            'PortofoliosCurrencies', "WHERE portofolio=? AND currency=?")
        cursor = self.connection.cursor()
        cursor.execute(sql_instruction, (portofolio_id, currency_id))
        if commit:
            self.connection.commit()

    def delete_transactions(self, ids: list[int], commit: bool = True):
        cursor = self.connection.cursor()
        values = [(id_, ) for id_ in ids]
        cursor.executemany(
            delete('CryptoTransaction', "WHERE idTransaction=?"), values)
        if commit:
            self.connection.commit()

    def commit(self):
        """Commit change"""
        self.connection.commit()
        self.LOGGER.debug('all changed are commited')

    def open(self):
        """Close the current connection if it's opened and create a new connection."""
        self.close()
        if not self.PATH.exists():
            raise errors.ConnectionDatabaseError(self.PATH)
        self.connection = sqlite3.connect(self.PATH.resolve(),
                                          detect_types=sqlite3.PARSE_DECLTYPES)
        self.connection.row_factory = _dict_factory
        self.LOGGER.debug('connection opened')

    def close(self):
        """Close the connection to the database."""
        if self.connection:
            self.connection.close()
        self.LOGGER.debug('connection closed')

    @classmethod
    def init_database(cls, remove_existing: bool = False):
        """Initialize the database.
        Use sqlite Python module because Qt don't allow the sqlite file creation.

        Parameters
        ----------
        remove_existing : bool, optional
            if True and that the database file exists, remove this file.
        """

        if not remove_existing and cls.PATH.exists():
            raise errors.DatabaseAlreadyExists(cls.PATH)

        elif cls.PATH.exists():
            cls.remove()

        try:
            conn = sqlite3.connect(cls.PATH, detect_types=sqlite3.PARSE_DECLTYPES)

            cursor = conn.cursor()

            script_file = QFile(":/sql/init_db")
            script_file.open(QIODevice.ReadOnly | QIODevice.Text)
            cursor.executescript(str(script_file.readAll(), 'utf-8'))
            script_file.close()

            conn.commit()
        except sqlite3.OperationalError as e:
            cls.LOGGER.error(f"Error during the database initialization: {e}")
            raise errors.DatabaseError(f"Error during the database initialization: {e}")
        finally:
            if conn:
                conn.close()

    @classmethod
    def remove(cls):
        """Remove the sqlite database file."""
        cls.PATH.unlink(missing_ok=True)
        cls.LOGGER.warning(f"Database {cls.PATH} was deleted")

    @classmethod
    def create_connection(cls):
        """Create a new connection to the database.

        Parameters
        ----------
        name : str
            The connection name
        """
        if not cls.PATH.exists():
            raise errors.ConnectionDatabaseError(cls.PATH)
        conn = sqlite3.connect(cls.PATH.resolve(), detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = _dict_factory
        cls.LOGGER.debug("Connection to the database created")
        return cls(conn)
