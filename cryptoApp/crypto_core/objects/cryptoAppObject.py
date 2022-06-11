

class CryptoAppObject:
    """Base class for all object of CryptoApp.py

    Properties
    ----------
    id : Any, getter only
        id of object in database
    """

    def __init__(self, id_):
        self._id = id_

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}(id: {self._id})>"

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def id(self):
        """Object id in database.
        """
        return self._id
