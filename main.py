from afd import AFD
def lerArquivoAF(arquivo):
    with open(arquivo, "r") as file:
        linhas = file.read().split('\n')
        nEstados = linhas[0]
        estadoInicial = linhas[1]
        estadosFinais = linhas[2].split(',')
        alfabeto = linhas[3].split(',')
        transicoes = []
        for linha in linhas[4:]:
            transicoes.append(linha.split(','))
    rodrigo = AFD([str(i) for i in range(int(nEstados))], alfabeto, estadoInicial, estadosFinais)
    for t in transicoes:
        rodrigo.addTransicao(t[0],t[1],t[2])

    while(True):
        try:
            s = input()
            print(rodrigo.computar(s))
        except EOFError:
            break

arquivo = input('nome do arquivo:\n')
lerArquivoAF(arquivo)
