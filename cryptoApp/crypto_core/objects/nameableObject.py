from . import CryptoAppObject


class NameableObject(CryptoAppObject):
    """Base class for nameable objects"""

    def __init__(self, id_, name: str):
        super().__init__(id_)
        self.name = name

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}(id: {self._id}, name: {self.name})>"

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        if not isinstance(name, str):
            raise ValueError(f"'name' must be a str, not {type(name)}")
        self._name = name
