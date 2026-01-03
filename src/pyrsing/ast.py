from abc import ABC

void = [" ", "\t", "\n", "\r\n"]

class ASTNode(ABC):

    def __init__(self):
        self.name:str = ''
        self.children:list = []
        self.parent:ASTNode = None
        self.is_optional:bool = False
        self.is_negation:bool = False
        self.is_repeat:bool = False

    def __str__(self):
        return str(self.__class__) \
            + f"{' NAME ' + self.name if self.name else ''}" \
            + f"{' OPTIONAL' if self.is_optional else ''}" \
            + f"{' REPEATER' if self.is_repeat else ''}" \
            + f"{' NEGATION' if self.is_negation else ''}"

    def print_tree(self, level=0, prefix="", is_last=True):
        """
        Print the token tree in a visual way using
        ASCII characters.
        """
        # prefix for current node
        if level == 0:
            line = str(self)
        else:
            conector = "└─" if is_last else "├─"
            line = f"{prefix}{conector} {str(self)}"
        line = [line]
        # new prefix for children
        if level > 0:
            prefix += "    " if is_last else "│   "
        for i, child in enumerate(self.children):
            last = i == len(self.children) - 1
            if isinstance(child, ASTNode):
                line.append(child.print_tree(level + 1, prefix, last))
            else:
                conector = "└─" if last else "├─"
                line.append(f"{prefix}{conector} '{str(child)}'")
        tree = "\n".join(line)
        if level>0:
            return tree
        print(tree + "\n")

class RootNode(ASTNode):
    """
    ()
    """
    def __init__(self):
        super().__init__()
        self.name:str = '__root__'
        self.parent:ASTNode = None
        self.is_optional:bool = False
        self.is_negation:bool = False
        self.is_repeat:bool = False

class TerminalNode(ASTNode):
    """
    ()
    """
    def __init__(self):
        super().__init__()
        self.name:str = '__terminal__'

class GroupNode(ASTNode):
    """
    ()
    """
    def __init__(self):
        super().__init__()
        self.name:str = '__group__'

class AlternativeNode(ASTNode):
    """
    ...|...|...
    """
    def __init__(self):
        super().__init__()
        self.name:str = '__alternative__'
