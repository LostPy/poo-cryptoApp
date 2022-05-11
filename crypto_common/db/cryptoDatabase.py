from pathlib import Path
from datetime import datetime
import sqlite3
import __main__

from PySide6.QtSql import QSqlDatabase, QSqlQuery

from crypto_common import errors
from .sql_instructions import create_table, insert


class CryptoDatabase:
    """Class to work with the 'crypto.db' sqlite database.
    """

    # The database is in the "root" of project
    PATH: Path = Path(__main__.__file__).parent / 'crypto.db'

    # Currency to init
    # TODO: Change this tuple in Currency object
    BASE_CURRENCIES = [
        ("dollar", "usd", 0),
        ("euro", "eur", 0)
    ]

    def __init__(self, connection: QSqlDatabase):
        self.connection: QSqlDatabase = connection

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

        conn = sqlite3.connect(cls.PATH)
        cursor = conn.cursor()

        cursor.execute(create_table(
            "Portofolio",
            [
                "idPortofolio integer PRIMARY KEY",
                "name text NOT NULL",
                "password text NOT NULL"
            ]
        ))
        cursor.execute(create_table(
            "Currency",
            [
                "idCurrency integer PRIMARY KEY",
                "name text NOT NULL",
                "ticker text",
                "datePrice timestamp",
                "logo text",
                "circulatingSupply integer",
                "rank integer",
                "isCrypto boolean Not NULL CHECK (isCrypto IN (0, 1))"
            ]
        ))
        cursor.execute(create_table(
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

        cursor.executemany(
            insert("Currency", ["name", "ticker", "isCrypto"]),
            cls.BASE_CURRENCIES  # TODO: change tuple in currency objects
        )
        conn.commit()
        conn.close()

    @classmethod
    def remove(cls):
        """Remove the sqlite database file."""
        cls.PATH.unlink(missing_ok=True)

    @classmethod
    def create_connection(cls, name: str) -> QSqlDatabase:
        """Create a new connection to the database.

        Parameters
        ----------
        name : str
            The connection name
        """
        conn = QSqlDatabase.addDatabase("QSQLITE", name)
        conn.setDatabaseName(str(cls.PATH.resolve()))
        return conn

    @staticmethod
    def get_connection(name: str, open_: bool = True) -> QSqlDatabase:
        """Get an existing connection (create previously with \
        `QSqlDatabase.addDatabase` or `CryptoDatabase.create_connection`). \
        If `open` is True and the database connection is not already \
        open it is opened now.

        Parameters
        ----------
        name : str
            The connection name
        open_ : bool, optional
            If True and the database connection is not already \
            open it is opened now. By default `open = True`
        """
        return QSqlDatabase.database(name, open_)

    @staticmethod
    def open_connection(connection: QSqlDatabase) -> 'None':
        """Open a connection if it is not already opened.

        Parameters
        ----------
        connection : QSqlDatabase
            The connection to open
        """
        if connection.isOpen():
            return

        if not connection.open():
            raise errors.ConnectionDatabaseError(connection.databaseName())
