from __future__ import annotations
from abc import ABC, abstractmethod
from pyrsing.token import TokenSequence
from pyrsing.exception import NotMatchException

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

    def set_pos(self, i:int):
        self.__i=i

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
        self._name:str = ''
        self.children:list = []
        self.parent:ASTNode = None
        self._is_optional:bool = False
        self.is_negation:bool = False
        self.is_repeat:bool = False
        self.num_repeat:int = 0
        self._current = None

    def __iter__(self):
        """
        Initialize iterator for depth-first traversal.
        """
        self._iter_stack = list(reversed(self.children))  # start with children reversed for stack order
        self._current = None
        return self

    def __next__(self):
        if not self._iter_stack:
            raise StopIteration
        node = self._iter_stack.pop()
        self._current = node
        if type(node) is str:
            return node
        # add children in reverse order to simulate stack behavior
        for child in reversed(node.children):
            self._iter_stack.append(child)
        return node

    @property
    def current(self):
        """
        Returns the current item during iteration, or None if not iterating.
        """
        if self._current is None:
            return self.children[0] if self.children else None
        return self._current

    def __str__(self):
        return f"<{self.__class__.__name__}>" \
            + f"{' OPTIONAL' if self.is_optional else ''}" \
            + f"{' REPEATER' if self.is_repeat else ''}" \
            + f"{' NEGATION' if self.is_negation else ''}"
    
    def parse(self, input:Input):
        input.rewind(0)
        return self._parse(input)

    def _parse(self, input:Input):
        start_pos = input.get_pos()
        try:
            if self.is_repeat:
                return self._parse_loop(input)
            return self._parse_element(input)
        except Exception as e:
            if self.is_optional:
                input.set_pos(start_pos)
                return None 
            raise e

    def _parse_loop(self, input:Input):
        num_rep:int = 0
        result=[]
        while True:
            input_pos:int = input.get_pos()
            try:
                item=self._parse_element(input)
                if isinstance(item, list):
                    result.extend(item)
                else:
                    result.append(item)
                num_rep+=1
                if self.num_repeat>0 and num_rep==self.num_repeat:
                    break
            except Exception as e:
                input.set_pos(input_pos)
                if self.num_repeat and num_rep<self.num_repeat:
                    if self.is_optional:
                        return result
                    raise NotMatchException(f"Did not achieve the expected number of repetitions. {self.num_repeat} repetitions were expected, but only {num_rep} were performed.")
                if num_rep==0 and not self.is_optional:
                    raise e
                break
        return TokenSequence(name=None, children=result)

    @abstractmethod
    def _parse_element(self, input:Input):
        pass
    
    @property
    def name(self)->str:
        """
        """
        return self.__class__.__name__ if not self._name else self._name
    
    @name.setter
    def name(self, val:str):
        self._name = val

    @property
    def is_optional(self, up:bool=False)->bool:
        """
        """
        if self._is_optional:
            return True
        elif up:
            parent = self.parent
            while parent:
                if parent.is_optional(up):
                    return True
                parent = parent.parent
        return False
    
    @is_optional.setter
    def is_optional(self, val:bool):
        self._is_optional = val

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

