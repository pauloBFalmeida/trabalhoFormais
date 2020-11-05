from afd import *
from afnd import *
from gr import *
from defreg import *
from er import *

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
        if len(linha) == 0:
            break
        transicoes.append(linha.split(','))

    rodrigo = criarAFND(nEstados, alfabeto, estadoInicial, estadosFinais, transicoes)
    # rodrigo.minimizar()
    # print()
    return rodrigo
    # geraldo = rodrigo.converterParaGR()
    # geraldo.printar()
    # print()
    # augusto = geraldo.converterParaAFND()
    # augusto.printar()
    # rodrigo.eliminarInalcancaveis()
    # rodrigo.printar()
    # print()

    # rodrigo.eliminarMortos()
    # rodrigo.printar()

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
    kilan = alberto.converterParaAFND()
    kilan.printar()
    #alberto.exportarParaArquivo(input('nome arquivo: '))

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

    julia = ER(linhas)
    for e in julia.instancias:
        # print(f"e = {e}" )
        # print(julia.instancias[e].expressoes)
        # julia.instancias[e].prepararExpressao()
        #julia.instancias[e].criarArvore()
        #julia.instancias[e].printarArvore()
        julia.instancias[e].converterParaAFD()
        julia.instancias[e].printarArvore()

print('lendo ER')
arquivo = input()
lerArquivoER(arquivo)


#lerArquivoGR(input())

# print('lendo afnd')
# arquivo1 = input()
# rodrigo = lerArquivoAF(arquivo1)
# rodrigo.printar()
# print('determinizar')
# damian = rodrigo.determinizar()
# damian.printar()
# print('ajustar nomes')
# damian.ajustarNomeEstados()
# damian.printar()
# print('uniao')
# eustaquio = damian.uniao(damian).uniao(damian)
# eustaquio.printar()
# print('ajustar nomes')
# eustaquio.ajustarNomeEstados()
# eustaquio.printar()
# print('minimizar')
# eustaquio.minimizar()
# eustaquio.printar()
# print('ajustar nomes')
# eustaquio.ajustarNomeEstados()
# eustaquio.printar()
# print('nome do arquivo para exportar para um arquivo:')
# eustaquio.exportarParaArquivo(input())


# eustaquio = rodrigo.uniao(rodrigo).uniao(rodrigo)
# eustaquio.minimizar()
# eustaquio.printar()
# rodrigo.printar()
#rodrigo.reduzirParaEquivalencia()

# arquivo2 = input()
# euclidio = lerArquivoAF(arquivo2)
# fausto = rodrigo.interseccao(euclidio)
# fausto.printar()
# fausto = fausto.uniao(fausto)
# fausto.printar()

#while True:
#    s = input()
#    print(fausto.computar(s))
