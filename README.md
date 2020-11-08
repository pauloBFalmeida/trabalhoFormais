Universidade Federal de Santa Catarina
Departamento de Informática e Estatística
Alunos: Paulo Barbato Fogaça de Almeida, Wesly Carmesini Ataide
Data: 07/11/2020

Para a elaboração deste trabalho usamos a linguagem Python.

Detalhes sobre a modelagem:

Nos autômatos finitos, cada um dos estados é representado como um string. Para o conjunto de estados, o conjunto do alfabeto e o conjunto de estados finais, usamos o set do Python, que implementa justamente o conjunto, para facilmente evitar repetições. As transições são representadas com um dicionário, que a chave sendo um estado e o valor um outro dicionário em que as chaves são os símbolos do alfabeto e o valor um conjunto contendo os estados para os quais o autômato transita com o estado e o símbolo especificado. No caso do autômato finito determinístico, o conjunto pode ter apenas um elemento. 
Para as gramáticas regulares, novamente usamos os conjuntos para os não terminais e os terminais, e um dicionário para as produções, com a chave do dicionário sendo o lado esquerdo da produção e levando para um conjunto de produções possíveis.
No caso das expressões regulares precisamos de uma abordagem mais complexa: temos uma classe ER que engloba várias definições, que são instanciadas nas classe DefReg. Como podemos ter referências entre as definições, fazemos que a classe ER trate de cuidar dessas referências, através de um dicionário que mantenha a DefReg de cada expressão.
Quando estamos convertendo de uma ER para um AFD, precisamos criar uma árvore usando a expressão da definição. Para isso, usamos a classe Nodo, que especifica um nodo de tal árvore, incluindo seus filhos e parâmetros como firstpos e lastpos.
