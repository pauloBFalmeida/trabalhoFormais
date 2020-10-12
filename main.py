from afd import AFD
from afnd import AFND

def criarAFD(nEstados, alfabeto, estadoInicial, estadosFinais, transicoes):
    afd = AFD([str(i) for i in range(int(nEstados))], alfabeto, estadoInicial, estadosFinais)
    for t in transicoes:
        afd.addTransicao(t[0],t[1],t[2])
    return afd

def criarAFND(nEstados, alfabeto, estadoInicial, estadosFinais, transicoes):
    afnd = AFND([str(i) for i in range(int(nEstados))], alfabeto, estadoInicial, estadosFinais)
    for t in transicoes:
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
        transicoes.append(linha.split(','))

    #rodrigo = criarAFD(nEstados, alfabeto, estadoInicial, estadosFinais, transicoes)
    rodrigo = criarAFND(nEstados, alfabeto, estadoInicial, estadosFinais, transicoes)

    while(True):
        try:
            s = input()
            print(rodrigo.computar(s))
        except EOFError:
            break

arquivo = input('nome do arquivo:\n')
lerArquivoAF(arquivo)
