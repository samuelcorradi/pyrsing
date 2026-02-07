from pyrsing.grammar import Grammar
from pyrsing import Input
from pyrsing.token import TokenSequence

def test_negation_operator_a_group_inside_sequence():
    """
    In this test we define in the root rule a right
    terminal followed by a negation of a group
    that contains a sequence of terminals.
    The input provided matches the first terminal
    but does not match the negated group, which
    is the expected behavior.
    The test asserts that the parsing result is as
    expected, confirming that the negation operator
    works correctly within a sequence.
    """
    g = Grammar({
            '__root__':'a (!aaa)'
        })
    ast_tree = g.ast_builder()
    input_data = Input('a zzz')
    cst_tree:TokenSequence = ast_tree.parse(input_data)
    result = cst_tree.to_primitive()
    assert result == {'__root__':['a zzz']}