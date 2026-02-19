
from pprint import pprint
import pytest
from pyrsing.grammar import Grammar
from pyrsing import Input

def parser(grammar:Grammar, input_str:str):
    """
    Helper function to create an AST builder from a grammar
    and parse an input string, returning the resulting AST.
    """
    ast_tree = grammar.ast_builder()
    # ast_tree.print_tree()
    input_data = Input(input_str)
    cst_result = ast_tree.parse(input_data)
    result = cst_result.to_primitive()
    pprint(result)
    return result

def test_builtins():
    """
    """
    from pyrsing.grammar import builtins
    new_rules = {
          '__root__':'(<breakline>|<space>|<decimal:>|<integer:>)+'
    }
    g = Grammar({**builtins, **new_rules})
    input_doc = """12

3.14
"""
    result = parser(g, input_doc)
    # assert
    assert result=={'__root__': [
              {'integer': ['12']}
            , '\n\n'
            , {'decimal': ['3.14']}
            , '\n'
        ]}

