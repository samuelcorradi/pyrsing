
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

@pytest.fixture
def rules():
    """
    """
    return {
          'text':'(!\n|__|~~|\\*\\*|_|\\*)+'
        , "bold":"\\*\\*(<text>)\\*\\*|__(<text>)__"
        , "italic":"_(<text>)_|\\*(<text>)\\*"
        , "strike":r'~~(<text>)~~'
        , 'paragraph':'(<strike:>|<bold:>|<italic:>|<text>)+'
    }

def test_transform(rules):
    """
    """
    g = Grammar({
              'paragraph':rules['paragraph']
            , 'bold':rules['bold']
            , 'italic':rules['italic']
            , 'strike':rules['strike']
            , 'text':rules['text']
            , 'regra':'[<paragraph:>|\n]+'
            , '__root__':'<regra:>'
        })
    input_doc = """Paragraph 1

Minha citação **bonita**.

"""
    result = parser(g, input_doc)
    # assert
    assert result=={'__root__': [
          {'paragraph': ['Paragraph 1']}
        , '<br /><br />'
        , {'paragraph': ['Minha citação ', 'BOLD', '.']}
        , '<br /><br />'
        ]}

