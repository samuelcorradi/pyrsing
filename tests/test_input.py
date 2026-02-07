from pyrsing import Input

def test_foreach_item_input():
    input_data = Input("Hello, World!")
    for char in input_data:
        print("Iterated character:", char)
    assert input_data.is_eol()

def test_input_class():
    input_data = Input("Hello, World!")
    assert input_data.input_str == "Hello, World!"
    assert input_data.get_pos() == 0
    assert input_data.peek() == 'H'
    next_char = next(input_data)
    assert next_char == 'H'
    assert input_data.get_pos() == 1
    assert input_data.peek_prev() == 'H'
    assert not input_data.is_eol()
    for char in input_data:
        print("Iterated character:", char)
    assert input_data.is_eol()