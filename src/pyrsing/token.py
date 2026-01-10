from __future__ import annotations
from dataclasses import dataclass
from typing import List, Union, Dict


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
    children: List[ParseNode]
    
    def to_primitive(self) -> List:
        result = []
        buffer = ""
        for c in self.children:
            if isinstance(c, Token):
                buffer += c.to_primitive()
            else:
                if buffer:
                    result.append(buffer)
                    buffer = ""
                result.append(c.to_primitive())
        if buffer:
            result.append(buffer)
        return result

@dataclass
class RuleNode:
    """
    Non-Terminal/Rule Node: resultado de uma production rule
    """
    name: str  # nome da regra
    children: List[ParseNode]
    
    def to_primitive(self) -> Dict:
        val = []
        buffer = ""
        for c in self.children:
            if isinstance(c, Token):
                buffer += c.to_primitive()
            else:
                if buffer:
                    val.append(buffer)
                    buffer = ""
                val.append(c.to_primitive())
        if buffer:
            val.append(buffer)
        return {self.name: val}

ParseNode = Union[Token, TokenSequence, RuleNode]