from . import CryptoException


class DatabaseException(CryptoException):
    """Exception raised for error related to the database.
    """
    pass


class DatabaseAlreadyExists(CryptoException):
    """Exception raised during the initialization \
    when the database file already exists.
    """

    def __init__(self, path: str):
        """file must be the filename of database."""
        super().__init__(f"The database '{str(path)}' already exists.")


class ConnectionDatabaseError(DatabaseException):
    """Exception raised when the connection to the database failed.
    """

    def __init__(self, name: str):
        """name must be the database name."""
        super().__init__(f"Can't connect to this database: '{name}'."
                         " Check if the database was initialized.")


class DbRequestMissingData(DatabaseException):
    """Exception raised when missing data in a request to the db (update or insert).
    """

    def __init__(self, data: str):
        super().__init__(f"Missing data to complete the request: '{data}'")
