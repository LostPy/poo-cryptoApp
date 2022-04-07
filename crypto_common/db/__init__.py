import sqlite3 as sql

from . import sql_instructions


def connection(dbname: str, ext: str = "db") -> sql.Connection:
    return sql.connect(f"{dbname}.{ext}")
