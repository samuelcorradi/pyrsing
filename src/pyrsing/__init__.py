from __future__ import annotations
from abc import ABC, abstractmethod

WHITESPACE_CHARS = [" ", "\t", "\n", "\r\n"]

class Input():

    def __init__(self
        , input_str:str):
        self.__i = 0
        self.input_str = input_str
    
    def __iter__(self):
        return self
    
    def __next__(self):
        self.__i += 1
        try:
            return self.input_str[self.__i-1]
        except IndexError:
            raise StopIteration # done iterating.
    next = __next__ # python2.x compatibility.

    def rewind(self, i:int=0):
        self.__i = i

    def get_pos(self):
        return self.__i

    def prev(self):
        self.__i += -1
        return self

    def peek(self)->str:
        """
        """
        return self.input_str[self.__i]
    
    def peek_prev(self)->str:
        """
        Retorna o valor anterior ao atual.
        Se o valor atual for o primeiro,
        retorna o primeiro valor mesmo.
        """
        return self.input_str[0 if (self.__i-1)<0 else self.__i-1]
    
    def hasNext(self)->bool:
        """
        """
        return self.__i<len(self.input_str)
    
    def parse(self, ast_node:ASTNode):
        self.rewind(0)
        return ast_node.parse(self)

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
    
    def parse(self, input):
        from pyrsing import Input # avoid circular import
        if type(input) is not Input:
            raise Exception("input must be an instance of Input or str.")
        return self.__parse(input)
    
    @abstractmethod
    def _parse(self, input):
        pass

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

class ASTRoot(ASTNode):
    """
    """
    def __init__(self):
        super().__init__()
        self.name:str = '__root__'
        self.parent:ASTNode = None
        self.is_optional:bool = False
        self.is_negation:bool = False
        self.is_repeat:bool = False

    def _parse(self, input):
        return None