from pyrsing import Input
from pyrsing.nodes import TerminalNode, SequenceNode, TokenSequence

def test_construct_ast_tree_without_grammar_and_parse_it():
    # create a sequence as root
    seq_node = SequenceNode()
    # create a terminal node
    terminal_node = TerminalNode('a')
    # add terminal as sequence child simulanting a ast grammar tree
    seq_node.children.append(terminal_node)
    # create input to use the "ast tree" to validate it
    input_data = Input('abc')
    # cst tree result after parser
    cst_result:TokenSequence = seq_node.parse(input_data)
    # result as Python primitive
    result = cst_result.to_primitive()
    # as the root is a sequence, the primitive is a list
    assert result == ['a']

def test_construct_ast_tree_with_named_root_without_grammar_and_parse_it():
    # create a sequence as root
    seq_node = SequenceNode('root')
    # create a terminal node
    terminal_node = TerminalNode('a')
    # add terminal as sequence child simulanting a ast grammar tree
    seq_node.children.append(terminal_node)
    # create input to use the "ast tree" to validate it
    input_data = Input('abc')
    # cst tree result after parser
    cst_result:TokenSequence = seq_node.parse(input_data)
    # result as Python primitive
    result = cst_result.to_primitive()
    # as the root is a sequence with name, the primitive is a dict
    assert result == {'root':['a']}