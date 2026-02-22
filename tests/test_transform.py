
from pprint import pprint
import pytest
# importing the on decorator and change its name to indicate that it is used for transformation
from pyrsing.transformer import on as on_decorator
from pyrsing.grammar import Grammar
from pyrsing import Input

def parser(grammar:Grammar, input_str:str):
    """
    Helper function to create an AST builder from a grammar
    and parse an input string, returning the resulting AST.
    """
    ast_tree = grammar.ast_builder()
    # ast_tree.print_tree()
    input_data = Input(input_str)
    cst_result = ast_tree.parse(input_data)
    result = cst_result.to_primitive()
    pprint(result)
    return result

@pytest.fixture
def rules():
    """
    """
    return {
          'text':'(!\n|__|~~|\\*\\*|_|\\*)+'
        , "bold":"\\*\\*(<text:>)\\*\\*|__(<text:>)__"
        , "italic":"_(<text:>)_|\\*(<text:>)\\*"
        , "strike":r'~~(<text:>)~~'
        , 'paragraph':'(<strike:>|<bold:>|<italic:>|<text>)+'
    }

def test_transform(rules):
    """
    This test show how to use the on decorator to
    transform a rule. We define in the transformer
    function that the elements from the text should
    be transformed to html tags. You can observe
    how we define the default set of rules
    separately and then merge them with the
    test-specific rules, this is a good practice to
    avoid code repetition and facilitate rule
    maintenance.
    """
    g = Grammar({**rules, **{
              'my_rule':'[<paragraph:>|\n]+' # defining my rule that will be transformed
            , '__root__':'<my_rule:>'
        }})
    input_doc = """Paragraph 1

Minha citação **bonita**.

"""
    result = parser(g, input_doc)
    # assert
    assert result=={'__root__': [
          {'paragraph': ['Paragraph 1']}
        , '<br /><br />'
        , {'paragraph': ['Minha citação <b>bonita</b>.']}
        , '<br /><br />'
        ]}

def test_even_if_the_rule_is_grouped_when_it_is_transformed_the_result_is_not_grouped():
    """
    This test shows how even if the rule transformed is
    grouped, the result of the transformation don't
    need necessarily be grouped. During the
    transformation, we can choose to return the rule
    result as a non-grouped. If we intend to keep the
    grouping, we can do it by returning as a dict, with
    the rule name as key or any other way that we
    prefer. Here we test the result of the same rule be
    returning in three different ways: not grouped,
    grouped with the value transformed to a single
    string and grouped changing the key from 'line' to
    'third_line'.
    """
    @on_decorator('my_grouped_rule')
    def my_grouped_rule_transformer(children:list):
        """
        Always when the rule 'my_grouped_rule' is matched,
        this function will be called and its children will
        be passed as argument.
        """
        result=[]
        for child in children:
            if isinstance(child, dict):
                for k, v in child.items():
                    if k == 'line' and v[0]=='First line.':
                        result.append(v)
                    elif k == 'line' and v[0]=='Second line.':
                        result.append({'line':''.join(v)})
                    elif k == 'line' and v[0]=='Third line.':
                        result.append({'third_line':v})
            else:
                result.append(child)
        return result

    g = Grammar({
              'line':'(!\n)+'
            , 'my_grouped_rule':'[\n|<line:>]' # defining my rule that will be transformed
            , '__root__':'<my_grouped_rule:>+'
        })
    input_doc = """First line.

Second line.

Third line.

"""
    result = parser(g, input_doc)
    # assert
    assert result=={'__root__': [
              ['First line.']
            , '\n\n'
            , {'line':'Second line.'}
            , '\n\n'
            , {'third_line':['Third line.']}
            , '\n\n'
        ]}

def test_how_transform_functions_are_applied_when_a_rule_has_an_alias():
    """
    This test shows how the transform functions
    are applied when a rule has an alias. As the
    transform funcion is executed only after when
    the as_primitive method is called, the alias
    is already applied to the rule, so the transform
    function will be applied to the rule with the
    alias name. In case that we have the same rule
    called in different places with different aliases,
    we can define different transform functions for
    each alias.
    """
    @on_decorator('my_grouped_alias')
    def my_grouped_rule_with_alias_transformer(children:list):
        """
        Always when the rule 'my_grouped_rule' has an alias
        'my_grouped_alias', this function will be called and
        its children will be passed as argument.
        """
        result=[]
        for child in children:
            if isinstance(child, dict):
                for k, v in child.items():
                    if k == 'line' and v[0]=='First line.':
                        result.append(v)
                    elif k == 'line' and v[0]=='Second line.':
                        result.append({'line':''.join(v)})
                    elif k == 'line' and v[0]=='Third line.':
                        result.append({'third_line':v})
            else:
                result.append(child)
        return result

    g = Grammar({
              'line':'(!\n)+'
            , 'my_grouped_rule':'[\n|<line:>]' # defining my rule that will be transformed
            , '__root__':'<my_grouped_rule:my_grouped_alias>+'
        })
    input_doc = """First line.

Second line.

Third line.

"""
    result = parser(g, input_doc)
    # assert
    assert result=={'__root__': [
              ['First line.']
            , '\n\n'
            , {'line':'Second line.'}
            , '\n\n'
            , {'third_line':['Third line.']}
            , '\n\n'
        ]}
