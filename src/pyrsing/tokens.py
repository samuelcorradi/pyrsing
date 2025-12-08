from pyrsing import Token

class Literal(Token):
    """
    ()
    """
    def __init__(self):
        super().__init__()

class Group(Token):
    """
    ()
    """
    def __init__(self):
        super().__init__()

class Or(Token):
    """
    ...|...|...
    """
    def __init__(self):
        super().__init__()
