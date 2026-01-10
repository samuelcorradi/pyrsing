"""
Example of how we can use token classes to build a CST results
tree and how we can use the to_primitive() method to convert
this tree of objects into the basic types of the language.
"""
from pyrsing.token import RuleNode, TokenSequence, Token

# <expr> -> "a" "b"
expr = RuleNode('expr', [Token('a'), Token('b')])
print(expr.to_primitive())  # {'expr': ['a', 'b']}

# <expr> -> ("a" "b")
expr_grouped = RuleNode('expr', [TokenSequence([Token('adasdas'), Token('b')])])
print(expr_grouped.to_primitive())  # {'expr': [['a', 'b']]}
