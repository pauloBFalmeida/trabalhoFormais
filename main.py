from afd import AFD
from afnd import AFND
from gr import GR

def criarAFD(nEstados, alfabeto, estadoInicial, estadosFinais, transicoes):
    afd = AFD([str(i) for i in range(int(nEstados))], alfabeto, estadoInicial, estadosFinais)
    for t in transicoes:
        afd.addTransicao(t[0],t[1],t[2])
    return afd

def criarAFND(nEstados, alfabeto, estadoInicial, estadosFinais, transicoes):
    afnd = AFND([str(i) for i in range(int(nEstados))], alfabeto, estadoInicial, estadosFinais)
    for t in transicoes:
        print(t)
        for estadosFinais in t[2].split('-'):
            afnd.addTransicao(t[0],t[1],estadosFinais)
    return afnd

def lerArquivoAF(arquivo):
    with open(arquivo, "r") as file:
        linhas = file.read().split('\n')

    nEstados = linhas[0]
    estadoInicial = linhas[1]
    estadosFinais = linhas[2].split(',')
    alfabeto = linhas[3].split(',')
    transicoes = []
    for linha in linhas[4:]:
        if len(linha) == 0:
            break
        transicoes.append(linha.split(','))

def lerArquivoGR(arquivo):
    with open(arquivo, "r") as file:
        linhas = file.read().split('\n')

    alberto = GR()
    for linha in linhas:
        if len(linha) <= 0:
            break
        linha = linha.split("->")
        simbolo = linha[0].strip()
        for c in linha[1]:
            if c.islower():
                alberto.addTerminal(c)
            elif c.isupper():
                alberto.addNaoTerminal(c)
        alberto.addNaoTerminal(simbolo)
        derivacoes = list(map(lambda x: x.strip(), linha[1].split("|")))
        for derivacao in derivacoes:
            alberto.addProducao(simbolo, derivacao)
    alberto.derivar(6)


    #rodrigo = criarAFD(nEstados, alfabeto, estadoInicial, estadosFinais, transicoes)
    # rodrigo = criarAFND(nEstados, alfabeto, estadoInicial, estadosFinais, transicoes)

    # while(True):
    #     try:
    #         s = input()
    #         print(rodrigo.computar(s))
    #     except EOFError:
    #         break

arquivo = input('nome do arquivo:\n')
lerArquivoGR(arquivo)
