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

# Template for `CREATE TABLE` instruction
CREATE_TABLE = """CREATE TABLE {name}
({columns})
"""

# Template for `INSERT` instruction
INSERT = """INSERT INTO {table} ({columns})
VALUES ({values})
"""

# Template for `UPDATE` instruction
UPDATE = """UPDATE {table}
SET {values}
"""

# Template for `SELECT` instruction
SELECT = """SELECT ({columns}) FROM {table}"""
ORDER_BY = """ORDER BY {column}"""  # Template for `ORDER_BY` instruction
WHERE = """WHERE {conditions}"""  # Template for `WHERE` instruction


def list_to_str(list_: list, str_in_items: bool = False) -> str:
    """Convert a list into a str (comma separated list).

    Parameters
    ----------
    list_ : list[Any]
        A list of items to convert into str
    str_in_items : bool, optional
        If True and there is str objects in the list, \
        add `"` for these objects in the string.

    Returns
    -------
    str
        The comma separated list of items
    """
    return ', '.join([
        f"\"{e}\"" if str_in_items and isinstance(e, str) and not e.startswith("'")
        else str(e)
        for e in list_
    ])


def dict_to_str(d: dict, separator: str = '=') -> str:
    """Convert a dictionary into a comma separated list of pair `key{separator}value`

    Parameters
    ----------
    d : dict
        The dictionary to convert into str
    separator : str, optional
        The separator of key/value to use (default: `"="`)

    Returns
    -------
    str
        The comma separated list of pair key / value
    """
    return ', '.join([
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


def insert(table: str, columns: list[str]) -> str:
    """Returns SQL instructions for an `UPDATE`

    Parameters
    ----------
    table : str
        The table's name
    columns : list[str]
        The list of columns in order of values

    Returns
    -------
    str
        The SQL instruction
    """
    return INSERT.format(
        table=table,
        columns=list_to_str(columns),
        values=('?, ' * len(columns)).removesuffix(', ')
    )


def update(table: str, values: dict, *, where: str = "") -> str:
    """Returns SQL instructions for an `UPDATE`

    Parameters
    ----------
    table : str
        The table's name
    values : dict
        values to update, in key the column's name and in value the new value
    where : str, optional
        The `WHERE` clause

    Returns
    -------
    str
        The SQL instruction
    """
    return UPDATE.format(table=table, values=dict_to_str(values))


def select(table: str, columns: list[str], /,
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


def where(conditions: dict[str, str]) -> str:
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
        f"""{column}{operator}{f"'{value}'" if isinstance(value, str) else value}"""
        for column, (operator, value) in conditions.items()
    ]
    return WHERE.format(conditions=list_to_str(list_conditions))


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
