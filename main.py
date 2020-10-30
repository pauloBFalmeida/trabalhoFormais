from afd import *
from afnd import *
from gr import *
from defreg import *

def criarAFD(nEstados, alfabeto, estadoInicial, estadosFinais, transicoes):
    afd = AFD([str(i) for i in range(int(nEstados))], alfabeto, estadoInicial, estadosFinais)
    for t in transicoes:
        afd.addTransicao(t[0],t[1],t[2])
    return afd

def criarAFND(nEstados, alfabeto, estadoInicial, estadosFinais, transicoes):
    afnd = AFND([str(i) for i in range(int(nEstados))], alfabeto, estadoInicial, estadosFinais)
    for t in transicoes:
        # print(t)
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

    rodrigo = criarAFD(nEstados, alfabeto, estadoInicial, estadosFinais, transicoes)
    rodrigo.printar()
    print()
    geraldo = rodrigo.converterParaGR()
    geraldo.printar()
    print()
    augusto = geraldo.converterParaAFND()
    augusto.printar()
    # for t in transicoes:
    #     # print(t)
    #     for estadosFinais in t[2].split('-'):
    #         afnd.addTransicao(t[0],t[1],estadosFinais)
    # while(True):
    #     try:
    #         # s
    #     try:
    #         # s = input()
    #         # print(rodrigo.computar(s))
    #         #s = set(list(map(int, input().split())))
    #         # print(rodrigo.destraduzir(rodrigo.traduzir(s)))
    #         # rodrigo.printEstados()
    #         # rodrigo.determinizar()
    #         break
    #     except EOFError:
    #         break = input()
    #         # print(rodrigo.computar(s))
    #         #s = set(list(map(int, input().split())))
    #         # print(rodrigo.destraduzir(rodrigo.traduzir(s)))
    #         # rodrigo.printEstados()
    #         # rodrigo.determinizar()
    #         break
    #     except EOFError:
    #         break



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

    alberto.printar()
    # alberto.derivar(6)


    #rodrigo = criarAFD(nEstados, alfabeto, estadoInicial, estadosFinais, transicoes)
    # rodrigo = criarAFND(nEstados, alfabeto, estadoInicial, estadosFinais, transicoes)
    # rodrigo.

    # while(True):
    #     try:
    #         s = input()
    #         print(rodrigo.computar(s))
    #     except EOFError:
    #         break

def lerArquivoER(arquivo):
    with open(arquivo, "r") as file:
        linhas = file.read().split('\n')

    for linha in linhas:
        if len(linha) != 0:
            l = linha.split(":")
            julia = DefReg(l[0], l[1][1:])


# lerArquivoAF(arquivo)

lerArquivoER(arquivo)
