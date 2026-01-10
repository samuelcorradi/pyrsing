from pyrsing import ASTNode, Input
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
        
    def parse(self, input:Input):
        try:
            inp_char = input.next()
            print(inp_char, '.')
        except StopIteration:
            raise NotMatchException(f"Expected any character in grammar, got end of input at position '{input.get_pos()}'.")

class ProductionRuleNode(ASTNode):
    """
    Production rule com nome: <rule_name>
    """
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    @staticmethod
    def parse_rule_name(rule_str:str)->tuple[str,str]:
        """
        Extracts the token name and alias (if any) from a rule.
        Returns a tuple (name, alias).
        Throws an exception if the syntax is incorrect.
        """
        mask = r'<([^>:]+)(:[^>]+)?>'
        match = re.match(mask, rule_str)
        if not match:
            raise Exception(f"Syntax error on rule '{rule_str}'.")
        token_name = match.group(1)
        alias = match.group(2)
        return token_name, alias

    def parse(self, input: Input):
        results = []
        for item in self.children:
            if isinstance(item, ASTNode):
                res = item.parse(input)
                results.append(res)
        if self.is_negation:
            raise NotMatchException("Negation matched when it should not have.")
        # senao, eh uma sequencia/grupo
        return RuleNode(self.name, results)

    def __str__(self):
        return f"<{self.__class__.__name__}:{self.name}>" \
            + f"{' OPTIONAL' if self.is_optional else ''}" \
            + f"{' REPEATER' if self.is_repeat else ''}" \
            + f"{' NEGATION' if self.is_negation else ''}"



class SequenceNode(ASTNode):
    """
    ()
    """
    def __init__(self, name:str=''):
        super().__init__()
        self._name = name

    def parse(self, input:Input):
        for item in self.children:
            if isinstance(item, ASTNode):
                item.parse(input)
        if self.is_negation:
            raise NotMatchException("Negation matched when it should not have.")

    def __str__(self):
        return f"<{self.name + ":" if self.name else ''}{self.__class__.__name__}>" \
            + f"{' OPTIONAL' if self.is_optional else ''}" \
            + f"{' REPEATER' if self.is_repeat else ''}" \
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
            + f"{' REPEATER' if self.is_repeat else ''}" \
            + f"{' NEGATION' if self.is_negation else ''}"

    def parse(self, input:Input):
        try:
            inp_char = input.next() # input.peek()
        except StopIteration:
            raise NotMatchException(f"Expected '{self.char}' in grammar, got end of input at position '{input.get_pos()}'.")
        print(inp_char, self.char)
        if inp_char == self.char:
            return
        else:
            raise NotMatchException(f"Expected '{self.char}' in grammar, got '{inp_char}' from input at position '{input.get_pos()}'.")

class GroupNode(ASTNode):
    """
    ()
    """
    def __init__(self):
        super().__init__()

    def parse(self, input:Input):
        for item in self.children:
            if isinstance(item, ASTNode):
                item.parse(input)

class OrNode(ASTNode):
    """
    ...|...|...
    """
    def __init__(self):
        super().__init__()

    def parse(self, input:Input):
        inital_pos = input.get_pos()
        for item in self.children:
            if isinstance(item, ASTNode):
                print(inital_pos)
                print("ITEM", item, item.parent)
                try:
                    item.parse(input)
                    print("Sucesso")
                    return
                except NotMatchException as e:
                    input.rewind(inital_pos)
                    print(e)
                    continue
        raise NoAlternativesException("No alternatives matched.")