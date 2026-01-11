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
        flat_children = []
        # Flattening se necessário: Se children contém listas aninhadas devido a repetições
        for c in self.children:
             if isinstance(c, list): flat_children.extend(c)
             else: flat_children.append(c)
        for c in flat_children:
            if isinstance(c, Token):
                buffer += c.to_primitive()
            
            elif isinstance(c, TokenSequence):
                # Se for uma sequencia puramente de tokens, tenta unificar
                primitivo = c.to_primitive()
                # Se o resultado for uma lista só de strings, e estavamos bufferizando strings
                # isso é complexo. Geralmente token sequences viram listas.
                # Para simplificar terminais repetidos (a+), eles retornam TokenSequence([Token(a), Token(a)...])
                
                # Se temos algo no buffer, salva antes de processar o nó complexo
                if buffer:
                    result.append(buffer)
                    buffer = ""
                # Adiciona o resultado complexo
                result.append(primitivo)
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