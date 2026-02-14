# Pyrsing

O módulo Pyrsing foi criado para permitir a operação de _parsing_ de inputs no formato String de acordo com as regras definidas por nós em uma gramática.

A motivação para o desenvolvimento deste módulo surgiu diante da necessidade de automatizar a interpretação de códigos SQL a fim de gerar documentações automáticas dos scripts, sem a necessidade de realizar a análise/leitura manual destes códigos.

A ideia é que, através da definição das regras que definem uma sintaxe SQL válida, através de uma gramática, o Pyrsing fosse ser capaz de "_interpretar_" o input, gerando no final uma estrutura de dados que indique nomes de tabelas, colunas, se há join, etc.

A operação de parser utiliza o conjunto de regras para tratar o input, fazendo distinção no seu conteúdo entre as estruturas indicadas pelas regras da gramática e, assim, possamos ter acesso as partes do input inicial para que permita o análise/uso posterior destes componentes extraídos da forma que o programador desejar. Tal qual fazemos com expressões regulares.

O módulo Pyrsing não gera documentações automaticas, ou sequer faz a análise dos códigos, mas ele é capaz de interpretar os trechos de um input que se enquadram em regras específicas, previamente criadas na forma de uma gramática, para que seja possível extrair do input os valores relevantes que permitam posteriormente a realização de análises sintática automáticas devido a categorização dos valores do input de acordo com cada regra da gramática usada.

**Mas e as expressões regulares?**

Podemos com as expressões regulares analisar inputs, valida-los de acordo com as regras indicadas pela expressão, e extrair as partes que nos interessa caso o formato do input seja válido. Sendo assim, por que não utilizar apenas expressões regulares?

Bem, expressões regulares são muito úteis em vários casos, mas quando se precisa dinamismo na interpretação de inputs em um ambiente pouco controlado, elas se mostram pouco flexíveis.

Nos casos que precisamos interpretar inputs extensos, como os comandos de uma linguagem inteira, comandos estes podendo ser fornecidos de forma pouco previsível (como em um ficheiro com os comandos do tipo DML, DDL, etc. aparecendo todos juntos), seria preciso criar inúmeras expressões regulares para interpretar os possíveis comandos.

Ao invés de criar-mos uma série de expressões regulares exóticas, o módulo Pyrsing procura fornecer um meio simplificado para que possamos criar as regras que deverão ser usadas para interpretar os inputs definindo regras gramáticais poderosas através de poucos operadores básicos.

**Componentes básicos**

A utilização do Pyrsing consiste em utilizar dois componentes principais: (1) o **Input**, que é o valor na forma de String em que desejamos realizar o parser (interpretar e capturar elementos desejados), e (2) uma **gramática**, que é o conjunto de regras definida pelo usuário que serão utilizadas pelo módulo para interpretar o input fornecido.











# Gramática

Quando recebemos um input (seja uma frase, um trecho de uma linguagem SQL, ou a definição de uma classe Java, etc.) para o computador ele é tão somente uma sequencia de caracteres. Para que o input seja "interpretado", ele precisa ter algum sentindo, este sentido é dado através da gramática.

A gramática é o nome dado a regra ou conjunto de regras que, quando submetidas ao input, dizem quais as regras o input obdece e, assim, sabemos interpretá-lo. É a aplicação das regras sobre o input que dá significado semântico ao que, inicialmente, era apenas uma string.

Pegue por exemplo uma frase qualquer, seja qual for o seu idioma nativo. Justamente por que sabes as regras do vosso idioma, consegues interpretar em uma frase, o que é o sujeito, o verbo, o tempo verbal, etc. 

Se não conhecermos as regras que ditam a comunicação, as frases passam a não ter sentido algum. Já tentaste interpretar uma sequencia de caracteres japoneses sem ter o conhecimento das regras que definem a comunicação entre os japoneses? Este é o poder em conhecer a gramática que valida um input.

**Sintaxe para construção de gramáticas (operadores)**

A utilização de uma _sintaxe_ básica que nos permita criar gramáticas variadas é que faz o módulo ser especial. Como podemos definir diferentes gramáticas, podemos utilizar o módulo Pyrsing para interpretar um grande número de inputs, desde que a gramática o define seja fornecido juntamente com o que deve ser analisado.

As gramáticas são definidas através de uma sintaxe básica, simples, com a utilização de caracteres reservados que indicam as operações que podem ser feitas para validar o input. Vamos chamar estes caracteres de **operadores gramáticais**.

Os operadores, por tanto, são os caracteres que indicam as _operações_ que deverão ser aplicadas sobre o input afim de validar se este input está de acordo com as regras "gramaticais". Os operadores são:

`[]` - opcional
`()` - agrupamentos
`*`, `+`, `{x}` - repetição
`.` - caracter coringa
`<>` - Operador de regra
`!` - negação
`|` - condicional
`\` - escape 

## Operadores gramaticáis

### Operador literal

Caracteres (como letras, números, etc.) podem ser usados para compor a gramática. O que estes operadores do tipo caracter fazem é comparar que no input existe um caracter literalmente igual.

Se nossa gramática for definida como `Casa`, o input esperado deve ser exatamente igual a `Casa`. Isso por que, para cada caractere, será verificado na posição correspondente no input que exista o mesmo caracter. Caso o input seja `casa` já teria falhado, já que `C` não é o mesmo que `c` ('c' minúsculo), e o input não seria enquadrado como sendo _parte desta gramática_.

Utilizamos caracteres literais quando queremos indicar exatamente o que espera-se que o input tenha em determinada posição. Isso é excelente quando quisermos definir constantes, palavras, ou qualquer sequencia de caracteres que seja desejável que um input válido tenha.

### Operador coringa

O operador coringa é aquele que irá indicar como válido qualquer caracter que seja utilizado no input. Este operador é indicado na forma de um `.` (ponto).

Pegando o exemplo anterior: se nossa gramática foi definida como `.asa`, e o input for `Casa` ou `casa` (como 'c' maiúsculo ou minúsculo), não importa: ambos os casos serão válidos. 

Isso por que, quando estamos a validar o input utilizando-se a nossa gramática, ao encontrar o operador `.`, o interpretador está sendo indicado a aceitar qualquer caracter literal na mesma posição onde encontra-se o operador coringa. 

Dessa forma, se o input for `raca`, `*aca`, `.aca`, `$aca`, etc., não importa, qualquer coisa será considerada válida.

Utilizamos este operador quando queremos dar liberdade ao input, já que não pode-se definir a priori o que se espera em determinada posição.

### Condição OU

As vezes precisamos que nossa gramática seja mais flexível, dando mais de uma única opções de input. Para isso temos um operador que funciona como um "OU", e é expresso na forma de um caracter `|` (pipe).

O caracter pipe é usado na gramática sempre que quisermos dar duas ou mais opções possíveis para nosso input.

Suponha-se que nossa gramática seja definida como `praia|campo`. O que estamos a dizer é que a sequencia de literais `praia` _ou_ `campo` são igualmente válidos.

Se quisermos dar mais opções basta adicionar outro `|` a definição da gramática: `praia|campo|espaço`.

Devemos utilizar o operador OU quando não sabemos exatamente o que será utilizado no input, mas sabemos de antemão as alternativas que sejam válidas.

### Operador opicional

Quando nossa gramática precisa flexível ao ponto de dar a opção de um valor ser usado ou não, devemos colocar estes valores entre `[ ]` (colchetes). Este operador irá considerar como opicional tudo que está dentro das chaves, funcionando como um agrupamento de coisas opicionais.

Por exemplo: suponha-se que a gramática seja definida como `Hello[ World]`. O que estamos a dizer é que nosso input deve sempre possui a sequencia de literais `Hello`, mas - opicionalmente - pode ou não ser acompanhada da palavra ` World`. Os inputs abaixo seriam considerados igualmente válidos:

- `Hello`
- `Hello World`

Este operador deve ser utilizado sempre nosso input possa adicionar uma informação que, caso ela não esteja, não seja o suficiente para considerar o input como inválido.

### Operador de repetição

Suponha-se que queres indicar através das gramática uma regra que indique que deva haver a repetição de algum elemento no input. Fazemos isso através do(s) operadore(s) de repetição que indicam que o elemento logo a sua esquerda repita. Temos três operadores diferentes para indicar repetição:

- `+` (mais) - indica que o elemento a esquerda do operador deve repetir, pelo menos, 1 vez.
- `*` (asterisco) - indica que o elemento a esquerda pode ou não repetir. Não é obrigatório a repetição. Se o elemento não repetir, não será considerado inválido.
- `{<numero de repetições>}` (abre e fecha chaves) - operador utilizado quando queremos indicar exatamente a quantidade de repetições esperadas. O operado indica um valor inteiro entre chaves, onde a quantidade de repetições deve ser exatamente igual a quantidade indicada. Exemplo: `{1}`, `{5}`, `{99}`, etc.

Por exemplo: suponha-se que temos uma gramática definida como `Vou caaaaair`. Sendo que temos apenas uma sequencia de literais indicado, onde `a` se repete, o input válido para este tipo de gramática seria uma cadeia de literais exatamente igual `Vou caaaaair`.

**Operador de repetição**

Mas se definirmos a gramática como `Vou ca+ir`, o que estamos a indicar é que o caracter `a` espera-se que repita. O input esperado ao utilizar o operador de repetição `+` (mais) pode ser:

- `Vou caair`
- `Vou caaaaair`
- `Vou caaaaaaaaaaaaaaaair`
- etc.

Todos os inputs acima seriam válidos pois eles indicam exatamente o que se espera com o operador `+`: que o elemento a esquerda do operador deve repetir 1 ou N vezes.

**Repetição opcional**

Já se a gramática indicar a repetição como `Vou ca*ir`, os inputs válidos serião:

- `Vou caair`
- `Vou caaaaair`
- `Vou caaaaaaaaaaaaaaaair`
- etc.
- `Vou cair`

Todos os inputs acima seriam válidos pois eles indicam exatamente o que se espera com o operador `*`: que o elemento a esquerda do operador repita 0 ou mais vezes. Se não houver repetição, não há problema, o input continuará sendo válido.

**Indicando o número de repetições**

Já se a gramática indicar a repetição como `Vou ca{5}ir`, o inputs válidos seria apenas:

- `Vou caaaaair`

Apenas o input acima seria considerado válido pois só ele atende a regra indicada pelo operador `{5}`: que o elemento a esquerda do operado repita e repita exatamente 5 (cinco) vezes. Quais quer outros inputs não seriam válidos.

### Agrupamento

Podemos utilizar `( )` (parenteses) para agrupar uma sequencia operadores e literais em nossa sintaxe. Dessa forma os elementos agrupados funcionarão como uma sub-regra dentro da nossa gramática e podemos aplicar operadores sobre esta sub-regra.

Por exemplo: até então indicamos que podemos utilizar o operador `+` para repetir o elemento a sua esquerda. Usamos a sintaxe `Vou ca+ir` indicando que o caracter `a` (que está a esquerda do operador de repetição) deveria repetir.

Agora suponha-se que queiramos indicar a repetição não de um único caractere, mas de toda uma sequencia de caracteres e operadores. A solução para isso é agrupar a sequencia gramátical que esperamos que repita. Se nossa gramática for `(Vou cair )+` o input esperado para isso seria algo como `Vou cair Vou cair ` ou `Vou cair Vou cair Vou cair Vou cair `, etc. Isso por que agrupamos uma sequencia, adicionamos o operador de repetição logo a sua direita, indicando que o grupo _é o elemento que deve repetir_.

Podemos inclusive ter uma gramática assim: `(Vou ca+ir )*`. Nela temos o caracter `a` indicado que deve repetir e o grupo também, um sendo obrigatório a sua repetição e outro sendo opcional, respectivamente. Neste caso os inputs válidos seriam:

- `Vou caair `
- `Vou caaaaair Vou caaair Vou caaaaaaaair`
- etc

Como podes ver, o caracter `a` sempre se repete conforme indicado mas a sequencia inteira agrupada pode ou não repetir.

> Observe também que os caracteres `( )` (parenteses) não são esperados no input. Eles são operadores que apenas indicam a gramática a regra de agrupamento e não são considerados literais. Para ter os caracteres `(` e `)` como literais, é necessário utilizar o operador de escape (`\`) antes de cada um deles.

Em resumo, o operador de agrupamento deve ser utilizado quando queremos considerar uma sequencia de operadores e literais como uma entidade única, para que se submetam todas elas a uma determinada regra.

### Operador de regra

Enquanto o operador de agrupamento (`( )`) nos permite definir uma sequencia de literais e operadores como uma regra unificada, as vezes queremos fazer o mesmo, mas de forma modular para que as regras possam ser reaproveitadas em diferentes locais na sintaxe. Temos uma solução para isso através do operador de regra `< >`.

### Operador de Negação

As vezes não queremos definir o que nosso input deve ter, mas o quê ele NÃO deve ser. Para estes casos temos o operador `!` (exclamação). O que este operador faz é inverter o resultado da avalição do input em comparação com a sintaxe.

Para que funcione, o Operador de Negação deve ser o primeiro caracter da regra. Se tentarmos usar `!` na regra que define a gramática, em qualquer outro local que não seja o caracter inicial, um erro de sintaxe será lançado.

Suponha-se que queiramos indicar que a sequencia de literais "sintaxe errada" não seja válida, definimos a regra da gramática como (observe como `!` está na posição inicial):

`!sintaxe errada`

Abaixo temos um exemplo de como não utilizar utilizar o Operador de Negação. Pois ele deveria estar na primeira posição da regra gramatical.

`sintaxe errada!`

Podemos usar o **Operador de Negação** dentro de um **Agrupamento**. Isso fará com que o input seja válido somente se ele não casar com a regra definida dentro do grupo em questão.

`meu literal (!sintaxe errada)`

Podemos também indicar a negação de uma regra que esteja sendo definida através de um **Operador de Regra**:

`meu literal <!sintaxe errada>`

Para utilizar o caracter **!** (exclamação) como um _literal_, é preciso utilizar antes dele o Operador de Escape.

**Exemplo de uso**

No exemplo abaixo vemos que a regra raiz (`__root__`) indica que o input, na parte indicada dentro do agrupamento, não pode ter terminais com a letra `a`.

```python
from pyrsing.grammar import Grammar
from pyrsing import Input
from pyrsing.token import TokenSequence

g = Grammar({
        '__root__':'a (!aaa)'
    })

root_ast = g.ast_builder()
input_data = Input('a zzz')
result:TokenSequence = root_ast.parse(input_data)
print(result.to_primitive())
```

Como nosso input indica `zzz` na parte onde temos uma negação (`(!aaa)`) a interpretação é válida e o resultado esperado são os valores detacados:

```python
{'__root__': ['a ', ['zzz']]}
```

Quando indicamos o input como `'a aaa'`, como estamos a indicar valores que estão sendo indicados como "proibidos" pelo operador de negação, o resultado da execução é uma exceção:

```
pyrsing.exception.NotMatchException: Negation sequence matched, which is not allowed.
```

### Operador de Escape

Como utilizamos caracteres para indicar as operações gramáticais, nem todos os caracteres indicados na gramática serão utilizados como um operador literal. Tome por exemplo o `.` (ponto) que é usado para indicar "qualquer caractere". Se utilizamos um ponto como operador para construir a gramática, como podemos fazer para exigir que o input tenha realmente um "ponto" em determinada posição?

A solução para isso é o caracter `\` (barra) na nossa gramática. O operador "ponto" irá indicar na gramática que o caracter a sua direita, seja ele qual for e não importa se ele seja um dos operadores básicos da gramática, ele deverá ser interpretado como um literal.

Se nossa gramática for definica como `\.asa` estamos a dizer que o "ponto" deve ser um ponto literal, e não se comportar como o operador coringa. Sendo assim, apenas o input `.asa` será considerado válido. Pois a gramática, com o ponto escapado, está a dizer que espera um ponto literal no local definido.

Devemos utilizar o operador `\` de escape sempre que precisarmos que um caracter que seja usado como operador seja considerado como um caracter literal no momento da validação de um input. 

Se precisamos utilizar uma barra como literal, então nossa gramática deve indicar isso com a utilização de duas barras `\\`. A mais a esqueda funcionando como um operador de escape para a barra a direita ser interpretada como uma barra, literalmente.

**Exemplo de uso**

O Operador de Negação consiste na utilização do caracter `!` (exclamação). Assim, se precisarmos definir o uso da exclamação como um literal (e não um operador) precisamos usar o Operador de Escape antes dele.

```python
from pyrsing.grammar import Grammar
from pyrsing import Input
from pyrsing.token import TokenSequence

g = Grammar({
        '__root__':'Hello\\!'
    })

ast_tree = g.ast_builder()
input_value = Input('Hello!')
result:TokenSequence = ast_tree.parse(input_value)
print(result.to_primitive())
```

Como utilizamos o operador de escape `\` (barra invertida) para indicar que `!` (exclamação) deve ser interpretado como um **literal**, o resultado da execução do código será:

```python
{'__root__': ['Hello!']}
```

Se não definirmos a regra como `'__root__':'Hello!'`, sem utilizar o **Operador de Escape**, o caracter de exclamação será interpretador como um **Operador de Negação**. O resultado da execução resultaria em uma exceção pois operadores de negação só podem ser usados como sendo o **primeiro caracter** de uma regra:

```
Exception: Negation can only be indicated at position 0. Use escape '\!' to include it as literal.
```
