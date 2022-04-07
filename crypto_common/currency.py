"""
Programme pour avoir le nom de la monnaie 

"""

class Currency:
    """Define the currency"""
    def __init__(self, id_: int, name: str):
        self.name = name
        self.id = id_
