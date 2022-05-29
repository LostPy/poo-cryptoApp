

class CryptoAppObject:
    """Base class for all object of CryptoApp"""

    def __init__(self, id_):
        self._id = id_

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}(id: {self._id})>"

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def id(self):
        return self._id
