from pyrsing import Input
from pyrsing.nodes import TerminalNode, TokenSequence

def test_parser_single_terminal_using_its_class_directly():
    # define a single input
    input_data = Input('abc fd')
    # first terminal
    terminal_node = TerminalNode('a')
    cst_tree:TokenSequence = terminal_node.parse(input_data)
    result:str = cst_tree.to_primitive()
    assert result == 'a'
    # a second terminal using same input
    terminal_node = TerminalNode('b')
    # let's use _parse because when we call parse, the input is rewound
    cst_tree:TokenSequence = terminal_node._parse(input_data)
    result:str = cst_tree.to_primitive()
    assert result == 'b'