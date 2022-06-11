"""Module with function to create SQL instructions.

Examples
--------

To create a table:
```python
create_table(
    name="User",
    columns=[
        "idUser INTEGER PRIMARY KEY",
        "name VARCHAR(20) NOT NULL",
    ]
)
```
"""

from typing import Union


# Template for `CREATE TABLE` instruction
CREATE_TABLE = """CREATE TABLE {name}
({columns})
"""

# Template for `INSERT` instruction
INSERT = """INSERT INTO {table} ({columns})
VALUES ({values})
"""

INSERT_OR_IGNORE = """INSERT OR IGNORE INTO {table} ({columns})
VALUES ({values})
"""

# Template for `UPDATE` instruction
UPDATE = """UPDATE {table}
SET {values}
"""

DELETE = """DELETE FROM {table}
{where}
"""

# Template for `SELECT` instruction
SELECT = """SELECT {columns} FROM {table}"""
ORDER_BY = """ORDER BY {column}"""  # Template for `ORDER_BY` instruction
WHERE = """WHERE {conditions}"""  # Template for `WHERE` instruction


def list_to_str(list_: list, str_in_items: bool = False, /, sep_char: str = ", ") -> str:
    """Convert a list into a str (comma separated list).

    Parameters
    ----------
    list_ : list[Any]
        A list of items to convert into str
    str_in_items : bool, optional
        If True and there is str objects in the list, \
        add `"` for these objects in the string.
    sep_char : str, optional, keyword only
        The separator of items

    Returns
    -------
    str
        The comma separated list of items
    """
    return sep_char.join([
        f"\"{e}\"" if str_in_items and isinstance(e, str) and not e.startswith("'")
        else str(e)
        for e in list_
    ])


def dict_to_str(d: dict, *, separator: str = '=', sep_items: str = ", ") -> str:
    """Convert a dictionary into a comma separated list of pair `key{separator}value`

    Parameters
    ----------
    d : dict
        The dictionary to convert into str
    separator : str, optional
        The separator of key/value to use (default: `"="`)
    sep_items : str, optional, keyword only
        The separator of items

    Returns
    -------
    str
        The comma separated list of pair key / value
    """
    return sep_items.join([
        f"""{column}{separator}{f"'{value}'" if isinstance(value, str) else value}"""
        for column, value in d.items()
    ])


def create_table(name: str, columns: list[str]) -> str:
    """Returns the SQL instruction to create a table

    Parameters
    ----------
    name : str
        The table's name to create
    columns : list[str]
        The list of column names

    Returns
    -------
    str
        The SQL instruction to create the table
    """
    return CREATE_TABLE.format(name=name, columns=list_to_str(columns))


def insert(table: str, columns: list[str],
           values: list = None, ignore: bool = False) -> str:
    """Returns SQL instructions for an `INSERT`

    Parameters
    ----------
    table : str
        The table's name
    columns : list[str]
        The list of columns in order of values
    values : list, optional
        values to insert (corresponding to the columns)
    ignore : bool, optional, default: False
        If True use the instruction `INSERT OR IGNORE`

    Returns
    -------
    str
        The SQL instruction
    """
    if values is not None:
        values = list_to_str(values, str_in_items=True)
    else:
        values = ('?, ' * len(columns)).removesuffix(', ')

    if ignore:
        return INSERT_OR_IGNORE.format(
            table=table,
            columns=list_to_str(columns),
            values=values
        )
    return INSERT.format(
        table=table,
        columns=list_to_str(columns),
        values=values
    )


def update(table: str, values: Union[list, dict], /, where: str = "") -> str:
    """Returns SQL instructions for an `UPDATE`

    Parameters
    ----------
    table : str
        The table's name
    values : Union[list, dict]
        values to update, if is a dict, keys are column's name and \
        values are the new value, if is a list, the elements are column names.
    where : str, optional
        The `WHERE` clause

    Returns
    -------
    str
        The SQL instruction
    """
    if isinstance(values, dict):
        values = dict_to_str(values)
    else:
        values = ', '.join([f'{column}=?' for column in values])
    return f"{UPDATE.format(table=table, values=values)}"\
           f"{where}"


def delete(table: str, where: str) -> str:
    """Returns SQL instructions for an `DELETE`

    Parameters
    ----------
    table : str
        The table's name
    where : str
        The `WHERE` clause

    Returns
    -------
    str
        The SQL instruction
    """
    return DELETE.format(table=table, where=where)


def select(table: str, columns: list[str], *,
           where: str = "", order_by: str = "") -> str:
    """Returns SQL instructions for a `SELECT`

    Parameters
    ----------
    table : str
        The table's name
    columns : list[str]
        Columns to get
    where : str, optional
        The `WHERE` clause
    order_by : str, optional
        The column use to sort data

    Returns
    -------
    str
        The SQL instruction
    """
    return f"{SELECT.format(table=table, columns=list_to_str(columns))} "\
           f"{where} {order_by}"


def where(conditions: dict[str, tuple[str, str]]) -> str:
    """Return SQL instructions for a `WHERE` clause.

    Parameters
    ----------
    conditions : dict[str, str]
        A dictionary with conditions: \
        keys are the column names and values are the operator to use.
        Example:
        ```python
        {
            "ColumnA": ('>', 10),
            "ColumnB": ("IN", "('a', 'b', 'c'')")
        }
        ```

    Returns
    -------
    str
        The instructions for the `WHERE`
    """
    list_conditions = [
        f"""{column} {operator} {f"'{value}'" if isinstance(value, str) else value}"""
        for column, (operator, value) in conditions.items()
    ]
    return WHERE.format(conditions=list_to_str(list_conditions, sep_char=' AND '))


def order_by(column: str) -> str:
    """Return the SQL instruction for a `ORDER BY` clause.

    Parameters
    ----------
    column : str
        The column's name

    Returns
    -------
    str
        The SQL instruction for `ORDER BY`
    """
    return ORDER_BY.format(column=column)
