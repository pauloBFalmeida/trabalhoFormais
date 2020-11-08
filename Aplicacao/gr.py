# -*- coding: utf-8 -*-
# Universidade Federal de Santa Catarina
# Departamento de Informática e Estatística
# Alunos: Paulo Barbato Fogaça de Almeida, Wesly Carmesini Ataide
# Data: 07/11/2020

from erros import *

class GR():

# ======= Criacao =========

    def __init__(self, simboloInicial='S', terminais=[], naoTerminais=[]):
        self.simboloInicial = simboloInicial
        self.terminais = set(terminais)
        self.naoTerminais = set(naoTerminais)
        self.producoes = {}

    def addTerminal(self, a):
        self.terminais.add(a)

    def addNaoTerminal(self, a):
        self.naoTerminais.add(a)

    def addProducao(self, simbolo, derivacao):
        if (len(derivacao) == 1 and derivacao not in self.terminais) or \
           (len(derivacao) == 2 and (derivacao[0] not in self.terminais or derivacao[1] not in self.naoTerminais) or \
           (len(derivacao) > 2)) or \
           (len(simbolo) != 1 or simbolo not in self.naoTerminais):
            raise GramaticaNaoRegular()
        if simbolo not in self.producoes:
            self.producoes[simbolo] = set()
        self.producoes[simbolo].add(derivacao)

    def remTerminal(self, a):
        if a in self.terminais:
            self.terminais.discard(a)
            for e in self.producoes:
                aRemover = set()
                for d in self.producoes[e]:
                    if a in d:
                        aRemover.add(d)
                self.producoes[e] = self.producoes[e].difference(aRemover)

    def remNaoTerminal(self, s):
        if s in self.naoTerminais:
            self.naoTerminais.discard(s)
            del self.producoes[s]
            for e in self.producoes:
                aRemover = set()
                for d in self.producoes[e]:
                    if s in d:
                        aRemover.add(d)
                self.producoes[e] = self.producoes[e].difference(aRemover)

    def remProducao(self, esquerdo, direito):
        if esquerdo in self.producoes:
            if direito in self.producoes[esquerdo]:
                self.producoes[esquerdo].discard(direito)

# ======= Derivacao =========

    def derivar(self, profundidadeMax):
        self.passoDerivacao([self.simboloInicial], profundidadeMax)

    def passoDerivacao(self, cadeia, nivel):
        # fim da recursao
        if nivel == 0:
            for c in cadeia:
                if c not in self.terminais:
                    return
            # print da cadeia toda
            print(''.join(cadeia))
            return
        # para cada elemento da cadeia
        for i in range(len(cadeia)):
            s = cadeia[i]
            # se for uma producao troco por suas producoes
            if s in self.naoTerminais and s in self.producoes:
                prods = self.producoes[s]
                for prod in prods:
                    prod = list(prod)
                    cadeia = cadeia[:i] + prod + cadeia[i+len(prod):]
                    self.passoDerivacao(cadeia, nivel-1)
                    cadeia = cadeia[:i] + [s] + cadeia[i+len(prod):]

# ======= Conversao para AFND =========

    def converterParaAFND(self):
        from afnd import AFND   # circular import se estiver fora do metodo
        # simbolo '#' representa o estado final
        automato = AFND(self.naoTerminais.union(set('#')),
                        self.terminais,
                        self.simboloInicial,
                        ["#"])
        # adiciono as transicoes no AF
        for simbolo in self.producoes:
            for prod in self.producoes[simbolo]:
                if len(prod) == 1:
                    automato.addTransicao(simbolo, prod[0], '#')
                else:
                    automato.addTransicao(simbolo, prod[0], prod[1])
        # ajusto os nomes e retorno o automato
        return automato

# ======= Ajustar nomes das Producoes =========

    def ajustarNomeProducoes(self):
        if len(self.naoTerminais) < 26:
            nomesNT = {self.simboloInicial: 'S'}
            letraAtual = 'A'
            naoTerminais = set('S')
            for nt in self.naoTerminais.difference(self.simboloInicial):
                nomesNT[nt] = letraAtual
                naoTerminais.add(letraAtual)
                letraAtual = chr(ord(letraAtual)+1)
            # atualizo os atributos
            self.naoTerminais = naoTerminais
            self.simboloInicial = 'S'
            # atualizo as producoes
            producoes = self.producoes
            self.producoes = {}
            for simbolo in producoes:
                for derivacao in producoes[simbolo]:
                    novoD = ""
                    for c in derivacao:
                        if c in self.terminais:
                            novoD += c
                        else:
                            novoD += nomesNT[c]
                    self.addProducao(nomesNT[simbolo], novoD)

# ======= Print no terminal =========

    def printar(self):
        simbolosNaoIniciais = [p for p in self.producoes if p != self.simboloInicial]
        simbolosNaoIniciais.sort()
        for simbolo in [self.simboloInicial] + simbolosNaoIniciais:
            l = simbolo + " -> "
            for prod in self.producoes[simbolo]:
                l += prod + " | "
            print(l[:-2])

# ======= Exportar para Arquivo =========

    def exportarParaArquivo(self, nomeArquivo):
        texto = ""
        # producoes
        for simbolo in self.producoes:
            texto += simbolo + " -> "
            for derivacao in self.producoes[simbolo]:
                texto += derivacao + " |"
            texto = texto[:-2] + '\n'
        # escrever no arquivo
        with open(nomeArquivo, 'w') as arquivo:
            arquivo.write(texto)
