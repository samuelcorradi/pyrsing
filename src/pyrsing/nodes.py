from __future__ import annotations
import re
from pyrsing import ASTNode, Input
from pyrsing.token import Token, TokenSequence
from pyrsing.exception import (
    NotMatchException,
    NoAlternativesException
)

class AnyNode(ASTNode):
    """
    ()
    """
    def __init__(self):
        super().__init__()
        
    def _parse_element(self, input:Input):
        try:
            inp_char = input.next()
        except StopIteration:
            raise NotMatchException(f"Expected any character in grammar, got end of input at position '{input.get_pos()}'.")
        return Token(inp_char)

class SequenceNode(ASTNode):
    """
    ()
    """
    def __init__(self, name:str=None):
        super().__init__()
        self._name = name

    @staticmethod
    def parse_rule_name(rule_str:str)->tuple[str,str]:
        """
        Extracts the token name and alias (if any) from a rule.
        Returns a tuple (name, alias).
        Throws an exception if the syntax is incorrect.
        """
        # allow an empty alias (e.g. <rule:>) so caller can signal grouping with no custom alias
        mask = r'<([^>:]+)(:[^>]*)?>'
        match = re.match(mask, rule_str)
        if not match:
            raise Exception(f"Syntax error on rule '{rule_str}'.")
        token_name = match.group(1)
        alias = match.group(2)
        return token_name, alias
    
    def _parse_element(self, input:Input):
        results = []
        error:ASTNode = None
        for item in self.children:
            if isinstance(item, TerminalNode) \
                and not item.is_repeat:
                char = input.peek()
                try:
                    _ = item._parse(input)
                    # if is executed, but it's a negation of the rule, it throws an error
                    if self.is_negation:
                        error = item
                except NotMatchException as e:
                    # if is executed, and it's a negation of the rule, it's ok
                    if not self.is_negation:
                        error = item
                results.append(Token(char))
            elif isinstance(item, TerminalNode):
                try:
                    res = item._parse(input)
                    results.append(res)
                    # if is executed, but it's a negation of the rule, it throws an error
                    if self.is_negation:
                        error = item
                except NotMatchException as e:
                    # if is executed, and it's a negation of the rule, it's ok
                    if not self.is_negation:
                        error = item
            elif isinstance(item, ASTNode):
                try:
                    res = item._parse(input)
                    results.append(res)
                    if self.is_negation:
                        error = item
                except NotMatchException:
                    if not self.is_negation:
                        error = item
        if error:
            if self.is_negation:
                raise NotMatchException(f"Negation sequence matched, which is not allowed.")
            else:
                if isinstance(error, TerminalNode):
                    raise NotMatchException(f"Expected '{error.char}' in sequence, but it did not match at position '{input.get_pos()}'.")
                raise NotMatchException(f"Sequence did not match. Error was: {error}")
        return TokenSequence(name=self._name, children=results)

    def __str__(self):
        name = self._name+':' if self._name else ''
        return f"<{name}{self.__class__.__name__}>" \
            + f"{' OPTIONAL' if self.is_optional else ''}" \
            + f"{' REPEATER' if self.is_repeat else ''}" + (f"({str(self.num_repeat)})" if self.num_repeat else '') \
            + f"{' NEGATION' if self.is_negation else ''}"

class TerminalNode(ASTNode):
    """
    ()
    """
    def __init__(self, char:str):
        super().__init__()
        self.char = char

    def __str__(self):
        return f"<{self.__class__.__name__}> '{self.char}'" \
            + f"{' OPTIONAL' if self.is_optional else ''}" \
            + f"{' REPEATER' if self.is_repeat else ''}" + (f"({str(self.num_repeat)})" if self.num_repeat else '') \
            + f"{' NEGATION' if self.is_negation else ''}"

    def _parse_element(self, input:Input):
        try:
            inp_char = next(input)
        except StopIteration:
            raise NotMatchException(f"Expected '{self.char}' in grammar, got end of input at position '{input.get_pos()}'.")
        if inp_char == self.char:
            return Token(inp_char)
        else:
            raise NotMatchException(f"Expected '{self.char}' in grammar, got '{inp_char}' from input at position '{input.get_pos()}'.")

class OrNode(ASTNode):
    """
    ...|...|...
    """
    def __init__(self):
        super().__init__()

    def _parse_element(self, input:Input):
        inital_pos = input.get_pos()
        for option in self.children:
            if isinstance(option, ASTNode):
                try:
                    res = option._parse(input)
                    return res
                except Exception as e:
                    input.rewind(inital_pos)
                    continue
        raise NoAlternativesException("No alternatives matched.")