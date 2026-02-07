
from pyrsing.grammar import Grammar
from pyrsing import Input
from pyrsing.token import ParseNode

def test_repeat_terminal_exact_3_times():
    """
    Testamos a forma de repetição onde indicamos na regra a quantidade exata que esperamos que o valor literal apareça no input.
    """
    g = Grammar({
            '__root__':'(a{3}a a)'
        })
    root_ast = g.ast_builder()
    root_ast.print_tree()
    input_data = Input('aaaa a')
    result:ParseNode = input_data.parse(root_ast)
    r = result.to_primitive()
    assert r == {'__root__': ['aaaa a']}

def test_repeat_a_terminal_inside_a_group_zero_or_many_times_followed_by_space_and_other_terminal():
    g = Grammar({
            '__root__':'(a* a)'
        })
    root_ast = g.ast_builder()
    root_ast.print_tree()
    input_data = Input('aaaa a')
    result:ParseNode = input_data.parse(root_ast)
    r = result.to_primitive()
    assert r == {'__root__': ['aaaa a']}

def test_repeat_a_terminal_inside_a_group_one_or_many_times():
    g = Grammar({
            '__root__':'(a)+'
        })
    root_ast = g.ast_builder()
    root_ast.print_tree()
    input_data = Input('aaaaa')
    result:ParseNode = input_data.parse(root_ast)
    r = result.to_primitive()
    assert r == {'__root__': ['aaaaa']}

def test_repeat_a_single_terminal_one_or_more_times():
    g = Grammar({
            '__root__':'a+'
        })
    root_ast = g.ast_builder()
    root_ast.print_tree()
    input_data = Input('aaaaa')
    result:ParseNode = input_data.parse(root_ast)
    r = result.to_primitive()
    assert r == {'__root__': ['aaaaa']}

def test_repeat_a_entire_role_one_or_many_time():
    g = Grammar({
            'teste':'ccc '
            , '__root__':'(<teste>+)'
        })
    root_ast = g.ast_builder()
    root_ast.print_tree()
    input_data = Input('ccc ccc ')
    result:ParseNode = input_data.parse(root_ast)
    r = result.to_primitive()
    assert r == {'__root__': ['ccc ccc ']}

