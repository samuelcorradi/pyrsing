from pyrsing import ASTNode

class SequenceNode(ASTNode):
    """
    ()
    """
    def __init__(self):
        super().__init__()
        self.name:str = '__sequence__'

    def _parse(self, input):
        pass

class GroupNode(ASTNode):
    """
    ()
    """
    def __init__(self):
        super().__init__()
        self.name:str = '__group__'

    def _parse(self, input):
        pass

class OrNode(ASTNode):
    """
    ...|...|...
    """
    def __init__(self):
        super().__init__()
        self.name:str = '__or__'

    def _parse(self, input):
        pass
