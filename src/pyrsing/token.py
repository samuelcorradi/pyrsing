from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional, Union, Dict
from pyrsing import transformer

@dataclass
class Token:
    """
    Token/Terminal: conteúdo bruto parseado do input
    """
    text: str
    
    def to_primitive(self) -> str:
        return self.text

@dataclass
class TokenSequence:
    """
    Composite/Grouping Node: agregação de elementos (ex: grupos com ())
    """
    name: Optional[str]  # rule name or alias
    children: List[ParseNode]
    
    def to_primitive(self) -> List:
        result = []
        buffer = ""
        flat_children = []
        # flattening if children contain nested lists due to repetitions
        for c in self.children:
             if isinstance(c, list): flat_children.extend(c)
             else: flat_children.append(c)
        for c in flat_children:
            if isinstance(c, Token):
                buffer += c.to_primitive()
            elif isinstance(c, TokenSequence):
                primitivo = c.to_primitive()
                # if the initial result is a list of strings, concatenate it to the buffer
                if isinstance(primitivo, list) and all(isinstance(x, str) for x in primitivo):
                    buffer += ''.join(primitivo)
                else:
                    if buffer:
                        result.append(buffer)
                        buffer = ""
                    result.extend(primitivo) if isinstance(primitivo, list) else result.append(primitivo)
            elif c is None:
                continue
            else:
                raise ValueError("Unknown ParseNode type: " + str(type(c)))
        if buffer:
            result.append(buffer)
        if self.name:
            if self.name in transformer.registry:
                return transformer.registry[self.name](result)
            return {self.name: result}
        return result

ParseNode = Union[Token, TokenSequence]