import pytest
from pyrsing.grammar import Grammar
from pyrsing import Input
from pyrsing.token import TokenSequence

def test_literal_terminal_with_special_character_not_scaped():
    """
    Here we are testing the case where we have a
    literal terminal with a special character that
    is not escaped. In this case, the parser should
    not recognize the literal as a valid terminal
    and should raise an exception.
    """
    g = Grammar({
            '__root__':'Hello!'
        })
    with pytest.raises(Exception):
        ast_tree = g.ast_builder()
        input_value = Input('Hello!')
        ast_tree.parse(input_value)

def test_literal_terminal_with_special_character_scaped():
    """
    In this test, we are checking the behavior of
    the parser when we have a literal terminal
    that includes a special character, but it is
    properly escaped. The parser should recognize
    the literal as a valid terminal and successfully
    parse the input.
    """
    g = Grammar({
            '__root__':'Hello\\!'
        })
    ast_tree = g.ast_builder()
    input_value = Input('Hello!')
    cst_tree:TokenSequence = ast_tree.parse(input_value)
    result = cst_tree.to_primitive()
    assert result == {'__root__':['Hello!']}