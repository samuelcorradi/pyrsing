
from pyrsing.grammar import Grammar
from pyrsing import Input
from pyrsing.token import ParseNode

def test_parser_with_groups_and_or_operator():
    g = Grammar({
        '__root__':'(bbb |(aa|z) zz) a'
    })
    ast_tree = g.ast_builder()
    input_data = Input('aa zz a')
    cst_tree = ast_tree.parse(input_data)
    result = cst_tree.to_primitive()
    assert result == {'__root__':['aa zz a']}

def test_parser_with_group_and_or_operator_and_repetition():
    g = Grammar({
        '__root__':'(aa|z)*'
    })
    ast_tree = g.ast_builder()
    ast_tree.print_tree()
    input_data = Input('zzzzz')
    cst_tree:ParseNode = input_data.parse(ast_tree)
    result = cst_tree.to_primitive()
    assert result == {'__root__':['zzzzz']}