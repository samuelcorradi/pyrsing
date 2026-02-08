"""
Example of how to implement a basic Markdown parser using pyrsing.
This example demonstrates how to define a grammar to parse common
Markdown elements, such as headings, lists, bold/italic text,
inline code, horizontal rules, and tables. The goal is to show
how to use pyrsing to create a parser for a popular text format.
"""
from pyrsing.grammar import Grammar
from pyrsing import Input
from pprint import pprint

g = Grammar({
          'number':'0|1|2|3|4|5|6|7|8|9'
        , 'lower':'a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z'
        , 'upper':'A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z'
        , 'space':' '
        , 'pontuacao':'\\&|\\.|,|;|:|\\!|\\?|\\-'
        , 'letter':'<lower>|<upper>'
        , 'word':'<letter>+'
        , 'integer':'<number>+'
        , 'text':'(<space>|<word>|<pontuacao>|<number>)*'
        , 'line':'(<bold:>|<italic:>|<space>|<word>|<pontuacao>)*'
        , 'multiline':'(\n|<line>)*'
        , 'title':'\\#<space><text>'
        , 'ul':'-<space><text>'
        , 'ol':'<number>. <text>'
        , 'list':'((<ul:>|<ol:>)+\n)+'
        , "bold":"\\*\\*(<text>)\\*\\*|\\_\\_(<text>)\\_\\_"
        , "italic":"_(<text>)_|\\*(<text>)\\*"
        , "code":"`<text>+`"
        , "hrule":"(\\*\\*\\*|---|___)"
        , 'blockcode':'```[<word:lang>]\n<text:>\n```'
        , 'tcell':'(<bold:>|<italic:>|<code:>|<text:>)*'
        , 'trow':'\\|(<tcell:>\\|)+\n'
        , 'tdiv':'\\| -( \\| -)* \\|\n'
        , 'table':'<trow:><tdiv><trow:>'
        , '__root__':'(\n|<table:>|<blockcode:>|<title:>|<list:>|<blockcode:>|<hrule:>|<code:>|<line:>|<multiline:>)+'
    })

sample_document = """# Title

Paragraph

- palavra
- palavra
- etc

1. palavra
1. palavra
1. etc.



```python
aghgjgjhgjhg jghg
```

Bold text **bold** and __bold__

Italic text *italic* and _italic_

---

***

___

| as | da |
| - | - |
| `ads` | **dsada** |

bb
"""

root_ast = g.ast_builder()
input_doc = Input(sample_document)
result_doc = root_ast.parse(input_doc)
pprint(result_doc.to_primitive())
