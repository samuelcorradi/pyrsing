from __future__ import annotations
from pyrsing import ASTNode

class Parser():

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
    
    def parse(self, root_node:ASTNode)->Parser:
        return Parser(self, root_node)
