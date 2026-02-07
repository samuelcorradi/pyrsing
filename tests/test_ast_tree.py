from pyrsing.grammar import Grammar

def test_ast_tree_generation_with_aliases(capsys):
    g = Grammar({
            'teste':'(c.c)'
            , '__root__':'(bbb |(aa|z)* zz <teste:alias>) a'
        })
    expected_tree = """<__root__:SequenceNode>
├─ <SequenceNode>
│   └─ <OrNode>
│       ├─ <SequenceNode>
│       │   ├─ <TerminalNode> 'b'
│       │   ├─ <TerminalNode> 'b'
│       │   ├─ <TerminalNode> 'b'
│       │   └─ <TerminalNode> ' '
│       └─ <SequenceNode>
│           ├─ <SequenceNode> OPTIONAL REPEATER
│           │   └─ <OrNode>
│           │       ├─ <SequenceNode>
│           │       │   ├─ <TerminalNode> 'a'
│           │       │   └─ <TerminalNode> 'a'
│           │       └─ <SequenceNode>
│           │           └─ <TerminalNode> 'z'
│           ├─ <TerminalNode> ' '
│           ├─ <TerminalNode> 'z'
│           ├─ <TerminalNode> 'z'
│           ├─ <TerminalNode> ' '
│           └─ <alias:SequenceNode>
│               └─ <SequenceNode>
│                   ├─ <TerminalNode> 'c'
│                   ├─ <AnyNode>
│                   └─ <TerminalNode> 'c'
├─ <TerminalNode> ' '
└─ <TerminalNode> 'a'

"""
    root_ast = g.ast_builder()
    root_ast.print_tree()
    result = capsys.readouterr()
    assert result.out == expected_tree

def test_ast_tree_generation_with_groups_and_without_aliases(capsys):
    """
    This test checks the generation of the AST
    tree when the grammar includes groups and
    does not use aliases.
    """
    g = Grammar({
            '__root__':'! (bbb | (aa|aaa) ccc)'
        })
    expected_tree = """<__root__:SequenceNode> NEGATION
├─ <TerminalNode> ' '
└─ <SequenceNode>
    └─ <OrNode>
        ├─ <SequenceNode>
        │   ├─ <TerminalNode> 'b'
        │   ├─ <TerminalNode> 'b'
        │   ├─ <TerminalNode> 'b'
        │   └─ <TerminalNode> ' '
        └─ <SequenceNode>
            ├─ <TerminalNode> ' '
            ├─ <SequenceNode>
            │   └─ <OrNode>
            │       ├─ <SequenceNode>
            │       │   ├─ <TerminalNode> 'a'
            │       │   └─ <TerminalNode> 'a'
            │       └─ <SequenceNode>
            │           ├─ <TerminalNode> 'a'
            │           ├─ <TerminalNode> 'a'
            │           └─ <TerminalNode> 'a'
            ├─ <TerminalNode> ' '
            ├─ <TerminalNode> 'c'
            ├─ <TerminalNode> 'c'
            └─ <TerminalNode> 'c'

"""
    root_ast = g.ast_builder()
    root_ast.print_tree()
    result = capsys.readouterr()
    assert result.out == expected_tree

def test_generating_ast_tree_using_parse_a_rule_expression(capsys):
    """
    This test checks the generation of the AST
    tree when the grammar includes groups and
    does not use aliases.
    """
    g = Grammar()
    expected_tree = """<__root__:SequenceNode> NEGATION
├─ <TerminalNode> ' '
└─ <SequenceNode>
    └─ <OrNode>
        ├─ <SequenceNode>
        │   ├─ <TerminalNode> 'b'
        │   ├─ <TerminalNode> 'b'
        │   ├─ <TerminalNode> 'b'
        │   └─ <TerminalNode> ' '
        └─ <SequenceNode>
            ├─ <TerminalNode> ' '
            ├─ <SequenceNode>
            │   └─ <OrNode>
            │       ├─ <SequenceNode>
            │       │   ├─ <TerminalNode> 'a'
            │       │   └─ <TerminalNode> 'a'
            │       └─ <SequenceNode>
            │           ├─ <TerminalNode> 'a'
            │           ├─ <TerminalNode> 'a'
            │           └─ <TerminalNode> 'a'
            ├─ <TerminalNode> ' '
            ├─ <TerminalNode> 'c'
            ├─ <TerminalNode> 'c'
            └─ <TerminalNode> 'c'

"""
    # _parser_rule returns a tuple (ASTNode, int)
    root_ast, n = g._parse_rule('! (bbb | (aa|aaa) ccc)')
    root_ast.print_tree()
    result = capsys.readouterr()
    assert result.out == expected_tree

def test_foreach_item_iterator_in_ast_tree():
    """
    An object of ASTNode can be iterated using a for loop,
    which traverses all its child nodes in preorder.
    This test checks that the iteration over the AST tree
    works correctly and that the nodes are visited in the
    expected order.
    """
    g = Grammar({
            '__root__':'! (bbb | (aa|aaa) ccc)'
        })
    ast_tree = g.ast_builder()
    ast_tree.print_tree()
    node_list = [str(ast_tree)]
    # traverses all nodes in preorder
    for node in ast_tree:
        node_list.append(str(node))
    assert node_list == [
          "<__root__:SequenceNode> NEGATION"
        , "<TerminalNode> ' '"
        , "<SequenceNode>"
        , "<OrNode>"
        , "<SequenceNode>"
        , "<TerminalNode> 'b'"
        , "<TerminalNode> 'b'"
        , "<TerminalNode> 'b'"
        , "<TerminalNode> ' '"
        , "<SequenceNode>"
        , "<TerminalNode> ' '"
        , "<SequenceNode>"
        , "<OrNode>"
        , "<SequenceNode>"
        , "<TerminalNode> 'a'"
        , "<TerminalNode> 'a'"
        , "<SequenceNode>"
        , "<TerminalNode> 'a'"
        , "<TerminalNode> 'a'"
        , "<TerminalNode> 'a'"
        , "<TerminalNode> ' '"
        , "<TerminalNode> 'c'"
        , "<TerminalNode> 'c'"
        , "<TerminalNode> 'c'"
    ]