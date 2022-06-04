

class CryptoException(Exception):

    def __init__(self, msg: str = ""):
        super().__init__()
        self.msg = msg

    def __str__(self) -> str:
        return f"{self.msg}"

    def __repr__(self) -> str:
        return self.__str__()


from .db import (
    DatabaseException,
    ConnectionDatabaseError,
    DatabaseAlreadyExists,
    DbRequestMissingData
)
