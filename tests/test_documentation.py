"""
Test file to validate all code examples from the README.md documentation.
This ensures that documentation examples are always working and up-to-date.
"""
import pytest
from pyrsing.grammar import Grammar
from pyrsing import Input
from pyrsing.token import TokenSequence
from pyrsing.exception import NotMatchException


class TestNegationOperator:
    """Tests for the Negation Operator examples in documentation."""
    
    def test_negation_valid_input(self):
        """Test negation operator with valid input (example from docs)."""
        g = Grammar({
            '__root__': 'a (!aaa)'
        })
        root_ast = g.ast_builder()
        input_data = Input('a zzz')
        result: TokenSequence = root_ast.parse(input_data)
        expected = {'__root__': ['a zzz']}
        assert result.to_primitive() == expected
    
    def test_negation_invalid_input(self):
        """
        Test negation operator with invalid
        input that should raise exception.
        """
        g = Grammar({
            '__root__': 'a (!aaa)'
        })
        root_ast = g.ast_builder()
        input_data = Input('a aaa')
        with pytest.raises(NotMatchException, match="Negation sequence matched"):
            root_ast.parse(input_data)


class TestEscapeOperator:
    """Tests for the Escape Operator examples in documentation."""
    
    def test_escape_exclamation_mark(self):
        """Test escape operator with exclamation mark (example from docs)."""
        g = Grammar({
            '__root__': 'Hello\\!'
        })
        
        ast_tree = g.ast_builder()
        input_value = Input('Hello!')
        result: TokenSequence = ast_tree.parse(input_value)
        
        expected = {'__root__': ['Hello!']}
        assert result.to_primitive() == expected


class TestRuleOperator:
    """Tests for the Rule Operator examples in documentation."""
    
    def test_basic_rule_reference(self):
        """Test basic rule reference syntax (example from docs)."""
        g = Grammar({
            'numero': '0|1|2|3|4|5|6|7|8|9',
            'digitos': '<numero>+',
            '__root__': '<digitos>'
        })
        
        ast_tree = g.ast_builder()
        input_data = Input('123')
        result = ast_tree.parse(input_data)
        
        primitives = result.to_primitive()
        assert '__root__' in primitives
        assert '1' in str(primitives)
        assert '2' in str(primitives)
        assert '3' in str(primitives)
    
    def test_rule_with_alias(self):
        """Test rule operator with alias for value capture (example from docs)."""
        g = Grammar({
            'numero': '0|1|2|3|4|5|6|7|8|9',
            'operacao': '<numero:esquerda> \\+ <numero:direita>',
            '__root__': '<operacao>'
        })
        
        ast_tree = g.ast_builder()
        input_data = Input('5 + 3')
        result = ast_tree.parse(input_data)
        
        primitives = result.to_primitive()
        # Verify that aliases are present in the result
        assert 'esquerda' in str(primitives)
        assert 'direita' in str(primitives)


class TestRecursiveGrammars:
    """Tests for recursive grammar examples in documentation."""
    
    def test_recursive_list_grammar(self):
        """Test recursive grammar (example from docs)."""
        g = Grammar({
            'lista': '- <texto>',
            'texto': '(!\n)+',
            '__root__': '<lista>'
        })
        
        ast_tree = g.ast_builder()
        input_data = Input('- item')
        result = ast_tree.parse(input_data)
        
        primitives = result.to_primitive()
        assert '__root__' in primitives


class TestGrammarClass:
    """Tests for Grammar class examples in documentation."""
    
    def test_grammar_basic_usage(self):
        """Test basic Grammar class usage (example from docs)."""
        g = Grammar({
            'numero': '0|1|2|3|4|5|6|7|8|9',
            '__root__': '<numero>+'
        })
        
        ast_tree = g.ast_builder()
        assert ast_tree is not None
        assert ast_tree.name == '__root__'


class TestInputClass:
    """Tests for Input class examples in documentation."""
    
    def test_input_basic_usage(self):
        """Test basic Input class usage (example from docs)."""
        g = Grammar({
            'numero': '0|1|2|3|4|5|6|7|8|9',
            '__root__': '<numero>+'
        })
        
        ast_tree = g.ast_builder()
        input_data = Input('12345')
        result = ast_tree.parse(input_data)
        
        assert result is not None


class TestTokenSequenceClass:
    """Tests for TokenSequence class examples in documentation."""
    
    def test_to_primitive_method(self):
        """Test to_primitive() method (example from docs)."""
        g = Grammar({
            'numero': '0|1|2|3|4|5|6|7|8|9',
            '__root__': '<numero>+'
        })
        
        ast_tree = g.ast_builder()
        input_data = Input('12345')
        result = ast_tree.parse(input_data)
        primitives = result.to_primitive()
        
        # Verify structure matches expected output
        assert '__root__' in primitives
        assert isinstance(primitives['__root__'], list)


class TestASTNodeClass:
    """Tests for ASTNode class examples in documentation."""
    
    def test_print_tree_method(self):
        """Test print_tree() method doesn't crash (example from docs)."""
        g = Grammar({
            'numero': '0|1|2|3|4|5|6|7|8|9',
            '__root__': '<numero>+'
        })
        
        ast_tree = g.ast_builder()
        
        # Should not raise any exception
        ast_tree.print_tree()


class TestCompleteWorkflow:
    """Tests for the complete workflow example in documentation."""
    
    def test_complete_workflow_example(self):
        """Test the complete workflow example from docs."""
        # 1. define the grammar
        g = Grammar({
            'number': '0|1|2|3|4|5|6|7|8|9',
            'operator': '\\+|\\-|\\*|/',
            'expression': '<number:left> <operator:op> <number:right>',
            '__root__': '<expression:>'
        })
        # 2. build the AST tree
        ast_tree = g.ast_builder()
        # 3. (optional) visualize the grammar structure
        ast_tree.print_tree()
        # 4. create the input to be parsed
        input_data = Input('5 + 3')
        # 5. parse the input
        result = ast_tree.parse(input_data)
        # 6. convert to Python structures
        primitives = result.to_primitive()
        # Verify the expected output structure
        expected = {'__root__': [
            {'expression': [
                      {'left': ['5']}
                    , ' '
                    , {'op': ['+']}
                    , ' '
                    , {'right': ['3']}
                ]}
            ]}
        assert primitives == expected
    
    def test_workflow_with_different_operators(self):
        """Test workflow with different mathematical operators."""
        g = Grammar({
            'number': '0|1|2|3|4|5|6|7|8|9',
            'operator': '\\+|-|\\*|/',
            'expression': '<number:left> <operator:op> <number:right>',
            '__root__': '<expression>'
        })
        
        test_cases = [
            ('5 + 3', '+'),
            ('7 - 2', '-'),
            ('4 * 6', '*'),
            ('8 / 2', '/'),
        ]
        
        for input_str, expected_op in test_cases:
            ast_tree = g.ast_builder()
            input_data = Input(input_str)
            result = ast_tree.parse(input_data)
            primitives = result.to_primitive()
            
            # Verify the operator was captured correctly
            assert expected_op in str(primitives)


class TestBestPractices:
    """Tests for best practices examples in documentation."""
    
    def test_alias_for_important_values(self):
        """Test using alias to identify important values."""
        g = Grammar({
            'palavra': '(!\n| )+',
            'comando_sql': 'SELECT <palavra:cols> FROM <palavra:tbl>',
            '__root__': '<comando_sql>'
        })
        
        ast_tree = g.ast_builder()
        input_data = Input('SELECT users FROM database')
        result = ast_tree.parse(input_data)
        primitives = result.to_primitive()
        
        # Verify aliases are present
        assert 'cols' in str(primitives)
        assert 'tbl' in str(primitives)
    
    def test_negation_for_anything_except(self):
        """Test negation operator for 'anything except' pattern."""
        g = Grammar({
            'string': '"(!\")*"',
            '__root__': '<string>'
        })
        
        ast_tree = g.ast_builder()
        input_data = Input('"hello world"')
        result = ast_tree.parse(input_data)
        primitives = result.to_primitive()
        
        assert '__root__' in primitives
        assert 'hello world' in str(primitives)
    
    def test_grouping_with_repetition(self):
        """Test combining grouping with repetition for complex patterns."""
        g = Grammar({
            'palavra': '(!\n|,| )+',
            'item': '<palavra>',
            'lista': '<item>(, <item>)*',
            '__root__': '<lista>'
        })
        
        ast_tree = g.ast_builder()
        input_data = Input('item1, item2, item3')
        result = ast_tree.parse(input_data)
        primitives = result.to_primitive()
        
        assert '__root__' in primitives
        # Verify all items are in the result
        result_str = str(primitives)
        assert 'item1' in result_str
        assert 'item2' in result_str
        assert 'item3' in result_str


class TestGrammarReusability:
    """Test that Grammar objects can be reused multiple times."""
    
    def test_grammar_multiple_ast_builds(self):
        """Test that calling ast_builder() multiple times works correctly."""
        g = Grammar({
            'numero': '0|1|2|3|4|5|6|7|8|9',
            '__root__': '<numero>+'
        })
        
        # Build AST multiple times
        ast_tree1 = g.ast_builder()
        result1 = ast_tree1.parse(Input('123'))
        
        ast_tree2 = g.ast_builder()
        result2 = ast_tree2.parse(Input('456'))
        
        # Both should work independently
        assert result1.to_primitive() != result2.to_primitive()
        assert '123' in str(result1.to_primitive())
        assert '456' in str(result2.to_primitive())
