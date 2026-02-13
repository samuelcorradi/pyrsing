"""
This file includes tests that aim to ensure the
library can handle markdown syntax, and that the
parsing result is as expected. The objective is to
verify if the markdown parser implementation is
capable of correctly recognizing language elements,
such as headings, lists, code blocks, bold and italic
text, among others, and if the resulting parsing
structure corresponds to the expected hierarchy and
organization for a markdown document.
"""
from pprint import pprint
import pytest
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
        , 'quote':r'\> <paragraph>'
        , 'paragraph':'(<strike:>|<bold:>|<italic:>|<text>|<inline_code:>)+'
        , 'number':r'0|1|2|3|4|5|6|7|8|9'
        , 'title':r'#+ <text>'
        , 'inline_code':r'`(!`|\n)*`'
        , 'block_code':'```\n[\n|(!(```))(!\n)*\n]*```'
        , 'ol':'<number>. <paragraph>'
        , 'ul':'- <paragraph>'
        , 'todo_item':'- \\[( |x)\\] <paragraph>'
        , 'todo_list':'(<todo_item:>+\n)+'
        , 'list':'((<ul:>|<ol:>)+\n)+'
        , 'hrule':"(\\*\\*\\*\\**|----*|____*)"
        , "bold":"\\*\\*(<text>)\\*\\*|__(<text>)__"
        , "italic":"_(<text>)_|\\*(<text>)\\*"
        , "strike":r'~~(<text>)~~'
        , 'tcell':'(!\n|\\|)+'
        , 'trow':'\\|(<tcell:>*\\|)+\n'
        , 'tsep':'\\|((-|:| )+\\|)+\n'
        , 'table':'<trow:thead><tsep>(<trow:>+)+'
        , 'link_alt':r'(!\])+'
        , 'link_url':r'(!\))+'
        , 'link':r'\[<link_alt:alt>\]\(<link_url:url>\)'
        , 'image':r'\!\[<link_alt:alt>\]\(<link_url:url>\)'
    }

def test_markdown_quote(rules):
    """
    """
    g = Grammar({
              'paragraph':rules['paragraph']
            , 'inline_code':rules['inline_code']
            , 'bold':rules['bold']
            , 'italic':rules['italic']
            , 'strike':rules['strike']
            , 'text':rules['text']
            , 'quote':rules['quote']
            , '__root__':'[<quote:>|<paragraph:>|\n]+'
        })
    input_doc = """Paragraph 1

> Minha citação **bonita**.

"""
    result = parser(g, input_doc)
    # assert
    assert result=={'__root__': [
          {'paragraph': ['Paragraph 1']}
        , '\n\n'
        , {'quote': [
                '> '
                , 'Minha citação '
                , {'bold': ['**bonita**']}
                , '.'
            ]}
        , '\n\n']}


def test_markdown_todo(rules):
    """
    """
    g = Grammar({
              'paragraph':rules['paragraph']
            , 'inline_code':rules['inline_code']
            , 'bold':rules['bold']
            , 'italic':rules['italic']
            , 'strike':rules['strike']
            , 'text':rules['text']
            , 'todo_item':rules['todo_item']
            , 'todo_list':rules['todo_list']
            , '__root__':'[<todo_list:>|<inline_code:>|<paragraph:>|\n]+'
        })
    input_doc = """Paragraph 1

![Minha imagem bonita.](https://www.bing.com/search?pglt=93FORM=ANNTA1&PC=U531)

- [ ] item 1
- [x] item 2 block 1


"""
    result = parser(g, input_doc)
    # assert
    assert result=={
        '__root__': [
              {'paragraph': ['Paragraph 1']}
            , '\n\n'
            , {'paragraph': ['![Minha imagem bonita.](https://www.bing.com/search?pglt=93FORM=ANNTA1&PC=U531)']}, '\n\n'
            , {'todo_list': [
                      {'todo_item': ['- [ ] item 1']}
                    , '\n'
                    , {'todo_item': ['- [x] item 2 block 1']}
                    , '\n'
                ]}
            , '\n\n'
        ]}

def test_markdown_image(rules):
    """
    """
    g = Grammar({
              'paragraph':rules['paragraph']
            , 'inline_code':rules['inline_code']
            , 'bold':rules['bold']
            , 'italic':rules['italic']
            , 'strike':rules['strike']
            , 'text':rules['text']
            , 'link_alt':rules['link_alt']
            , 'link_url':rules['link_url']
            , 'link':rules['link']
            , 'image':rules['image']
            , '__root__':'[<image:>|<link:>|<inline_code:>|<paragraph:>|\n]+'
        })
    input_doc = """Paragraph 1

![Minha imagem bonita.](https://www.bing.com/search?pglt=93FORM=ANNTA1&PC=U531)


"""
    result = parser(g, input_doc)
    # assert
    assert result=={
        '__root__': [{'paragraph': ['Paragraph 1']},
        '\n\n',
        {'image': ['![',
                {'alt': ['Minha imagem bonita.']},
                '](',
                {'url': ['https://www.bing.com/search?pglt=93FORM=ANNTA1&PC=U531']},
                ')']},
        '\n\n\n']}

def test_markdown_link(rules):
    """
    """
    g = Grammar({
              'paragraph':rules['paragraph']
            , 'inline_code':rules['inline_code']
            , 'bold':rules['bold']
            , 'italic':rules['italic']
            , 'strike':rules['strike']
            , 'text':rules['text']
            , 'link_alt':rules['link_alt']
            , 'link_url':rules['link_url']
            , 'link':rules['link']
            , '__root__':'[<link:>|<inline_code:>|<paragraph:>|\n]+'
        })
    input_doc = """Paragraph 1

[texto](https://www.bing.com/search?pglt=93FORM=ANNTA1&PC=U531)


"""
    result = parser(g, input_doc)
    # assert
    assert result=={
        '__root__': [{'paragraph': ['Paragraph 1']},
        '\n\n',
        {'link': ['[',
                {'alt': ['texto']},
                '](',
                {'url': ['https://www.bing.com/search?pglt=93FORM=ANNTA1&PC=U531']},
                ')']},
        '\n\n\n']}

def test_markdown_table(rules):
    """
    """
    g = Grammar({
              'paragraph':rules['paragraph']
            , 'inline_code':rules['inline_code']
            , 'bold':rules['bold']
            , 'italic':rules['italic']
            , 'strike':rules['strike']
            , 'text':rules['text']
            , 'trow':rules['trow']
            , 'tcell':rules['tcell']
            , 'tsep':rules['tsep']
            , 'table':rules['table']
            , '__root__':'[<table:>|<paragraph:>|\n]+'
        })
    input_doc = """Paragraph 1

|asd as| abbbb |
|-|-|
|dsa| dsa4 |
| dsa | dsa2 |


"""
    result = parser(g, input_doc)
    # assert
    assert result=={'__root__': [{'paragraph': ['Paragraph 1']},
              '\n\n',
              {'table': [{'thead': ['|',
                                    {'tcell': ['asd as']},      
                                    '|',
                                    {'tcell': [' abbbb ']},     
                                    '|',
                                    '\n']},
                         '|-|-|\n',
                         {'trow': ['|',
                                   {'tcell': ['dsa']},
                                   '|',
                                   {'tcell': [' dsa4 ']},       
                                   '|',
                                   '\n']},
                         {'trow': ['|',
                                   {'tcell': [' dsa ']},        
                                   '|',
                                   {'tcell': [' dsa2 ']},       
                                   '|',
                                   '\n']}]},
              '\n\n']}
    
def test_markdown_bold_italic(rules):
    """
    """
    g = Grammar({
              'paragraph':rules['paragraph']
            , 'inline_code':rules['inline_code']
            , 'bold':rules['bold']
            , 'italic':rules['italic']
            , 'strike':rules['strike']
            , 'text':rules['text']
            , '__root__':'[<paragraph:>|<bold:>|<italic:>|<strike:>|\n]+'
        })
    input_doc = """Paragraph 1

Paragraph 2 **bold** and __bold__

Paragraph ❤️ *italic* and _italic_

Paragraph com ~~paralavra riscada~~ no meio do texto.

"""
    result = parser(g, input_doc)
    # assert
    assert result=={
        '__root__': [
            {'paragraph': ['Paragraph 1']},
            '\n\n',
            {'paragraph': [
                'Paragraph 2 ',
                    {'bold': ['**bold**']},
                    ' and ',
                    {'bold': ['__bold__']}
                ]},
            '\n\n',
            {'paragraph': [
                    'Paragraph ❤️ ',
                    {'italic': ['*italic*']},
                    ' and ',
                    {'italic': ['_italic_']}
                ]},
            '\n\n',
            {'paragraph': [
                    'Paragraph com ',
                    {'strike': ['~~paralavra riscada~~']},      
                    ' no meio do texto.'
                ]},
            '\n\n'
        ]}

def test_markdown_block_code(rules):
    """
    """
    g = Grammar({
              'paragraph':rules['paragraph']
            , 'inline_code':rules['inline_code']
            , 'bold':rules['bold']
            , 'italic':rules['italic']
            , 'strike':rules['strike']
            , 'text':rules['text']
            , 'block_code':rules['block_code']
            , '__root__':'[<block_code:>|<paragraph:>|\n]+'
        })
    input_doc = """
```
dsadasasds f sdfsd fs
fsdfsdfs 3427643287
```
"""
    result = parser(g, input_doc)
    # assert
    expected_result = {'__root__': ['\n', {'block_code': ['```\ndasasds f sdfsd fs\nfsdfs 3427643287\n```']}, '\n']}
    assert result==expected_result

def test_markdown_hrule(rules):
    """
    """
    g = Grammar({
              'paragraph':rules['paragraph']
            , 'inline_code':rules['inline_code']
            , 'bold':rules['bold']
            , 'italic':rules['italic']
            , 'strike':rules['strike']
            , 'text':rules['text']
            , 'number':rules['number']
            , 'ol':rules['ol']
            , 'ul':rules['ul']
            , 'list':rules['list']
            , 'hrule':rules['hrule']
            , '__root__':'[<hrule:>|<paragraph:>|\n]+'
        })
    input_doc = """Paragraph 1

------------------

___

******

`Code block 1`
"""
    result = parser(g, input_doc)
    # assert
    expected_result = {'__root__': [
          {'paragraph': ['Paragraph 1']}
        , '\n\n'
        , {'hrule': ['------------------']}
        , '\n\n'
        , {'hrule': ['___']}
        , '\n\n'
        , {'hrule': ['******']}
        , '\n\n'
        , {'paragraph': ['`Code block 1`']}
        , '\n'
    ]}
    assert result==expected_result

def test_markdown_list(rules):
    """
    """
    g = Grammar({
              'paragraph':rules['paragraph']
            , 'inline_code':rules['inline_code']
            , 'bold':rules['bold']
            , 'italic':rules['italic']
            , 'strike':rules['strike']
            , 'text':rules['text']
            , 'number':rules['number']
            , 'ol':rules['ol']
            , 'ul':rules['ul']
            , 'list':rules['list']
            , '__root__':'[<inline_code:>|<list:>|<paragraph:>|\n]+'
        })
    input_doc = """Paragraph 1

- item 1
- item 2
- item 3

1. item 1
1. item 2
1. item 3

# Title 1
Paragraph ❤️

`Code block 1`
"""
    result = parser(g, input_doc)
    # assert
    expected_result = {'__root__': [
          {'paragraph': ['Paragraph 1']}
        , '\n\n'
        , {'list': [
              {'ul': ['- item 1']}
            , '\n'
            , {'ul': ['- item 2']}
            , '\n'
            , {'ul': ['- item 3']}
            , '\n'
            ]}
        , '\n'
        , {'list': [
              {'ol': ['1. item 1']}
            , '\n'
            , {'ol': ['1. item 2']}
            , '\n'
            , {'ol': ['1. item 3']}
            , '\n']}
        , '\n'
        , {'paragraph': ['# Title 1']}
        , '\n'
        , {'paragraph': ['Paragraph ❤️']}
        , '\n\n'
        , {'inline_code': ['`Code block 1`']}
        , '\n'
        ]
    }
    assert result==expected_result

def test_markdown_inline_code(rules):
    """
    Inline code is defined as a sequence of characters
    enclosed by backticks (`). The rule that defines an
    inline code is basically the mandatory repetition of
    any character that is not a line break or a backtick,
    enclosed by backticks.
    """
    g = Grammar({
              'paragraph':rules['paragraph']
            , 'bold':rules['bold']
            , 'italic':rules['italic']
            , 'strike':rules['strike']
            , 'text':rules['text']
            , 'inline_code':rules['inline_code']
            , '__root__':'[<inline_code:>|<paragraph:>|\n]+'
        })
    input_doc = """Paragraph 1

# Title 1
Paragraph ❤️

`Code block 1`
"""
    result = parser(g, input_doc)
    # assert
    expected_result = {'__root__': [{'paragraph': ['Paragraph 1']}, '\n\n', {'paragraph': ['# Title 1']}, '\n', {'paragraph': ['Paragraph ❤️']}, '\n\n', {'inline_code': ['`Code block 1`']}, '\n']}
    assert result==expected_result
    
def test_markdown_title(rules):
    """
    Headings are basically a paragraph that starts
    with one or more hash characters (#). The numbering
    of hashes indicates the heading level, where a
    level 1 heading has one hash, a level 2 heading
    has two hashes, and so on. The heading content is
    the text following the hashes, and can contain
    any sequence of characters, except line breaks.
    Therefore, the rule to define a heading is
    basically the mandatory repetition of hashes
    followed by a paragraph.
    """
    g = Grammar({
              'paragraph':rules['paragraph']
            , 'inline_code':rules['inline_code']
            , 'bold':rules['bold']
            , 'italic':rules['italic']
            , 'strike':rules['strike']
            , 'text':rules['text']
            , 'title':rules['title']
            , '__root__':'[<title:>|<paragraph:>|\n]+'
        })
    input_doc = """Paragraph 1

# Title 1
Paragraph ❤️

# Title 2"""
    result = parser(g, input_doc)
    # assert
    assert result=={'__root__': [{'paragraph': ['Paragraph 1']}, '\n\n', {'title': ['# Title 1']}, '\n', {'paragraph': ['Paragraph ❤️']}, '\n\n', {'title': ['# Title 2']}]}

def test_markdown_paragraph(rules):
    """
    The paragraph is defined as a sequence of
    characters that does not contain line breaks.
    Each continuous line is considered a paragraph.
    The rule that defines the paragraph is basically
    the mandatory repetition of any character that is
    not a line break. This rule is extremely
    generic, being able to capture any sequence of
    characters. Therefore, it should preferably be
    more to the right, being the last one to be
    evaluated by the parser.
    """
    g = Grammar({
              'paragraph':rules['paragraph']
            , 'inline_code':rules['inline_code']
            , 'bold':rules['bold']
            , 'italic':rules['italic']
            , 'strike':rules['strike']
            , 'text':rules['text']
            , '__root__':'[<paragraph:>|\n]+'
        })
    input_doc = """Paragraph 1

Paragraph 2
Paragraph ❤️"""
    result = parser(g, input_doc)
    print(result)
    # assert
    assert result=={'__root__':[{'paragraph': ['Paragraph 1']}, '\n\n', {'paragraph': ['Paragraph 2']}, '\n', {'paragraph': ['Paragraph ❤️']}]}
