from abc import ABC, abstractmethod

void = [" ", "\t", "\n", "\r\n"]

class Token():

    def __init__(self):
        self.name:str = ''
        self.childrens:list = []
        self.parent:Token = None
        self.optional:bool = False
        self.negation:bool = False
        self.repeat:bool = False

    def __str__(self):
        return str(self.__class__) \
            + f"{' NAME ' + self.name if self.name else ''}" \
            + f"{' OPTIONAL' if self.optional else ''}" \
            + f"{' REPEATER' if self.repeat else ''}" \
            + f"{' NEGATION' if self.negation else ''}"

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
        for i, child in enumerate(self.childrens):
            last = i == len(self.childrens) - 1
            if isinstance(child, Token):
                line.append(child.print_tree(level + 1, prefix, last))
            else:
                conector = "└─" if last else "├─"
                line.append(f"{prefix}{conector} '{str(child)}'")
        tree = "\n".join(line)
        if level>0:
            return tree
        print(tree + "\n")
