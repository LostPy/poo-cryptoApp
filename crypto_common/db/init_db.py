from . import sql
from .sql_instructions import create_table


def create_portofolio_table(conn: sql.Connection):
    cursor = conn.cursor()
    cursor.execute(create_table(
        "Portofolio",
        ["idPortofolio", "name", "password"]
    ))
