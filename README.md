# Pyrsing

Analise o codigo da pasta que anexo aqui. Eu tenho uma duvida conceitual sobre o caminho que o prgrama deve tomar daqui em diante.

Uma vez que meu codigo já consiga criar um AST a partir da gramática e validar um input, eu gostaria que fazer o parser dos trechos do input que correspondam a uma production rule na gramática.

Se na gramática esteja indicado (), isso quer dizer um agrupamento, entao o conteúdo no input neste trecho deverá está agrupado. Se o conteúdo do input for validado dentro de uma production rule (que aparece como <nome da rule>), o conteúdo do input que corresponde a esta regra também deverá ficar destacado, indicado a regra (production rule) que o destaca.

Minha duvida conceitual é, como representar o conteúdo resultante do parser? Eu poderia obter os resultados na forma de primitivos Python, com tudo em uma lista, grupos "()" aparecendo como listas dentro da lista [], e as production rules aparecendo como dicionarios, onde a chave é o nome da production rule e o valor um array, seguindo a lógica. 

Outra alternativa seria representar o resultado na forma de uma hierarquia, tal qual o AST, com objetos sendo usados para representar os valores. Mas nao sei se isso iria complicar. 

Tendo os conhecimentos sobre parser e conhecimento na criação de compiladores, qual a estrutura de dados resultante da operação de parser?

Eu poderia pergar o conteúdo resultante, analisar ele, otimizar alguma coisa, passar como parametro para classes externas que façam uso da informação extraída, etc.