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

    def imprimir_arvore(self, nivel:int=0, prefixo=""):
        """Imprime a árvore de forma visual usando caracteres ASCII."""
        r = [str(self.__class__) \
            + f"{' NAME' + self.name if self.name else ''}" \
            + f"{' OPTIONAL' if self.optional else ''}" \
            + f"{' REPEATER' if self.repeat else ''}" \
            + f"{' NEGATION' if self.negation else ''}"]
        for i, child in enumerate(self.childrens):
            line = (f"'{child.imprimir_arvore(nivel + 1)}'" if isinstance(child, Token) else str(child))
            line = f"{' |   '*(nivel)} " + ("└-" if i==len(self.childrens)-1 else "├-") + line
            r.append(line)
        return "\n".join(r)

                


