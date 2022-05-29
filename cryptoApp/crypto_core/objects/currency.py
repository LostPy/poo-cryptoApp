"""Class to define a currency
"""
from . import NameableObject


class Currency(NameableObject):
    """Define the currency"""

    def __init__(self, id_: int, name: str):
        super().__init__(id_, name)
