
import pytest
from pyrsing.grammar import Grammar
from pyrsing import Input
from pyrsing.exception import NoAlternativesException, NotMatchException

def test_or_node_with_third_option_right():
    # defing gramar with root rule as an option
    g = Grammar({
            '__root__':'bbb | aa | zzz z'
        })
    # gen the ast tree from grammar's rules
    ast_tree = g.ast_builder()
    # define a input equal any of these options
    input_data = Input(' zzz z')
    # parsing generating a cst tree with parsing result
    cst_result = ast_tree.parse(input_data)
    # result as primitive
    result = cst_result.to_primitive()
    # assert
    assert result=={'__root__':[' zzz z']}

def test_or_node_without_a_valid_option(capsys):
    """
    This test checks the behavior of the parser
    when the input does not match any of the
    alternatives defined in the grammar.
    It expects a NotMatchException to be
    raised, and it captures and prints the
    exception message and any output for
    verification.
    """
    # defing gramar with root rule as an option
    g = Grammar({
            '__root__':'bbb | aa | zzz z'
        })
    # gen the ast tree from grammar's rules
    ast_tree = g.ast_builder()
    # define a input equal any of these options
    input_data = Input(' xxx ')
    # parsing should raise NotMatchException because ' xxx ' doesn't match any alternative
    with pytest.raises(NotMatchException) as excinfo:
        ast_tree.parse(input_data)
    print(f"\nException caught: {excinfo.value}")
    captured = capsys.readouterr()
    print(f"\nCaptured output: {captured.out}")
        
