
from pyrsing.grammar import Grammar
from pyrsing import Input

def test_group_inside_group_inside_sequence():
    g = Grammar({
        '__root__':'bbb (aaa (ccc))'
    })
    ast_tree = g.ast_builder()
    ast_tree.print_tree()
    input_data = Input('bbb aaa ccc')
    ast_tree.parse(input_data)
