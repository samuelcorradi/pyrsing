
from pyrsing.grammar import Grammar
from pyrsing import Input
from pyrsing.token import ParseNode

def test_repeat_optional_inside_a_repeat_mandatory_with_right_input():
    """
    We tested a main rule that has a reference that needs
    to be repeated one or more times, but which points to
    another rule that is indicated to be repeated zero or
    more times, being optional. The goal is to test if the
    parser can handle an input where the optional part is
    repeated several times within the mandatory part, and
    if the parsing result is as expected.
    """
    g = Grammar({
            'inter_repeat':'(aaa)*'
            , '__root__':'(bbb <inter_repeat>+)'
        })
    root_ast = g.ast_builder()
    root_ast.print_tree()
    input_data = Input('bbb aaaaaa')
    result:ParseNode = input_data.parse(root_ast)
    r = result.to_primitive()
    assert r == {'__root__': ['bbb aaaaaa']}

def test_repeat_optional_inside_a_group_repeat_mandatory_with_right_input():
    """
    We tested a rule where we have a group that must be repeated one
    or more times, and inside it, we have a reference to a rule that
    can execute zero or more times. The goal of the test is to verify
    if multiple repetitions happen correctly when we indicate the
    expected values in the input, and what the behavior is when the
    input indicates an unexpected value, to see if the parser can
    handle this and return the expected result.
    """
    g = Grammar({
            'inter_repeat':'(aaa)*'
            , '__root__':'(bbb <inter_repeat>)+'
        })
    root_ast = g.ast_builder()
    root_ast.print_tree()
    input_data = Input('bbb aaaaaabbb aaabbb zzz')
    result:ParseNode = input_data.parse(root_ast)
    r = result.to_primitive()
    print(r)
    assert r == {'__root__': ['bbb aaaaaabbb aaabbb ']}

def test_repeat_optional_inside_a_repeat_mandatory_with_wrong_input():
    """
    This test involves a main rule that must be repeated
    at least once, and within that rule, there's an
    optional part that can be repeated zero or more times.
    The test verifies if the parser can correctly handle
    an input that doesn't contain the optional part but
    still satisfies the main rule.
    """
    g = Grammar({
            'inter_repeat':'(aaa)*'
            , '__root__':'(bbb <inter_repeat>+)'
        })
    root_ast = g.ast_builder()
    root_ast.print_tree()
    input_data = Input('bbb zzzzzz')
    result:ParseNode = input_data.parse(root_ast)
    r = result.to_primitive()
    assert r == {'__root__': ['bbb ']}

def test_repeat_terminal_exact_3_times():
    """
    We tested the repetition method where we specify
    in the rule the exact number of times we expect
    the literal value to appear in the input.
    The goal of the test is to verify if the parser
    can correctly handle this type of repetition and
    if it returns the expected result when the input
    matches the specified number of repetitions.
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

