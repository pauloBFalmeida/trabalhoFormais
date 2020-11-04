# -*- coding: utf-8 -*-
from erros import *
from gr import *

class AFD():

# ======= Criacao =========

    def __init__(self, estados, alfabeto, estadoInicial, estadosFinais):
        self.estados = set(estados)
        self.alfabeto = set(alfabeto)
        self.estadoInicial = estadoInicial
        self.estadosFinais = set(estadosFinais)
        self.transicoes = {}

    def addEstado(self, estado):
        self.estados.add(estado)

    def addAlfabeto(self, simbolo):
        self.alfabeto.add(simbolo)

    def addTransicao(self, estadoInicial, simbolo, estadoFinal):
        if not estadoInicial in self.estados:
            raise EstadoInexistente(str(estadoInicial))
        if not estadoFinal in self.estados:
            raise EstadoInexistente(str(estadoFinal))
        if not simbolo in self.alfabeto:
            raise SimboloInexistente(str(simbolo))

        if not estadoInicial in self.transicoes:
            self.transicoes[estadoInicial] = {}
        if not simbolo in self.transicoes[estadoInicial]:
            self.transicoes[estadoInicial][simbolo] = set()
        self.transicoes[estadoInicial][simbolo].add(estadoFinal)

# ======= Uniao e Interseccao =========

    def uniao(self, automato):
        estados = []
        estadosFinais = []
        for e in self.estados:
            for i in automato.estados:
                estados.append(e + " & "  + i)
                if e in self.estadosFinais or i in automato.estadosFinais:
                    estadosFinais.append(e + " & " + i)

        alfabeto = self.alfabeto.union(automato.alfabeto)

        estadoInicial = (self.estadoInicial + " & " + automato.estadoInicial)

        afdUniao = AFD(estados, alfabeto, estadoInicial, estadosFinais)

        for e in self.estados:
            if e not in self.transicoes:
                continue
            for i in automato.estados:
                if i not in automato.transicoes:
                    continue
                for c in alfabeto:
                    e_prox = '-'
                    i_prox = '-'
                    if c in self.transicoes[e]:
                        e_prox = list(self.transicoes[e][c])[0]
                    if c in automato.transicoes[i]:
                        i_prox = list(automato.transicoes[i][c])[0]
                    if e_prox != '-' and i_prox != '-':
                        estado_atual =  e +' & '+ i
                        estado_prox = e_prox +' & '+ i_prox
                        afdUniao.addTransicao(estado_atual, c, estado_prox)

        return afdUniao


    def interseccao(self, automato):
        estados = []
        estadosFinais = []
        for e in self.estados:
            for i in automato.estados:
                estados.append(e + " & "  + i)
                if e in self.estadosFinais and i in automato.estadosFinais:
                    estadosFinais.append(e + " & " + i)

        alfabeto = self.alfabeto.union(automato.alfabeto)

        estadoInicial = (self.estadoInicial + " & " + automato.estadoInicial)

        afdInterseccao = AFD(estados, alfabeto, estadoInicial, estadosFinais)

        for e in self.estados:
            if e not in self.transicoes:
                continue
            for i in automato.estados:
                if i not in automato.transicoes:
                    continue
                for c in alfabeto:
                    e_prox = '-'
                    i_prox = '-'
                    if c in self.transicoes[e]:
                        e_prox = list(self.transicoes[e][c])[0]
                    if c in automato.transicoes[i]:
                        i_prox = list(automato.transicoes[i][c])[0]
                    if e_prox != '-' and i_prox != '-':
                        estado_atual =  e +' & '+ i
                        estado_prox = e_prox +' & '+ i_prox
                        afdInterseccao.addTransicao(estado_atual, c, estado_prox)

        return afdInterseccao
    
# ======= Computar entrada =========

    def computar(self, s):
        estadoAtual = self.estadoInicial

        for c in s:
            if c not in self.alfabeto:
                raise SimboloInexistente(str(c))
            if c not in self.transicoes[estadoAtual]:
                raise TransicaoInexistente(str(estadoAtual), c)

            estadoAtual = list(self.transicoes[estadoAtual][c])[0]

        if estadoAtual in self.estadosFinais:
            return True
        return False

# ======= Converter para GR =========

    def converterParaGR(self):
        gramatica = GR(self.estadoInicial, list(self.alfabeto), list(self.estados))

        for estado in self.transicoes:
            for c in self.transicoes[estado]:
                gramatica.addProducao(str(estado), c + str(list(self.transicoes[estado][c])[0]))
                if list(self.transicoes[estado][c])[0] in self.estadosFinais:
                    gramatica.addProducao(str(estado), c)
        return gramatica

# ======= Minimizar =========

    def eliminarMortos(self):

        produtivos = self.estadosFinais

        while True:
            q = set()
            for e in self.transicoes:
                for c in self.transicoes[e]:
                    for s in self.transicoes[e][c]:
                        if s in produtivos and e not in produtivos:
                            q.add(e)
            produtivos = produtivos.union(q)
            if len(q) == 0:
                break

        self.estados = self.estados.intersection(produtivos)
        self.estadosFinais = self.estadosFinais.intersection(produtivos)

        novasTransicoes = {}

        for estado in self.transicoes:
            novasTransicoes[estado] = {}
            for c in self.transicoes[estado]:
                novasTransicoes[estado][c] = set()
                for s in self.transicoes[estado][c]:
                    if estado in produtivos and s in produtivos:
                        novasTransicoes[estado][c].add(s)

        self.transicoes = novasTransicoes


    def eliminarInalcancaveis(self):
        visited = set()
        visited.add(self.estadoInicial)
        current = [self.estadoInicial]

        while len(current) > 0:
            next = []

            for estado in current:
                if estado in self.transicoes:
                    for c in self.transicoes[estado]:
                        for s in self.transicoes[estado][c]:
                            if s not in visited:
                                next.append(s)
                                visited.add(s)

            current = next

        self.estados = self.estados.intersection(visited)
        self.estadosFinais = self.estadosFinais.intersection(visited)

        novasTransicoes = {}

        for estado in self.transicoes:
            novasTransicoes[estado] = {}
            for c in self.transicoes[estado]:
                novasTransicoes[estado][c] = set()
                for s in self.transicoes[estado][c]:
                    if estado in visited and s in visited:
                        novasTransicoes[estado][c].add(s)

        self.transicoes = novasTransicoes


    def reduzirParaEquivalencia(self):
        class Equivalencia():
            def __init__(self, estado):
                self.estado = estado
                self.classe_index = None
                self.transicoes = {}
            def setClasse(self, classe_index):
                self.classe_index = classe_index
            def getClasse(self):
                return classe_index
            def addTransicao(self, c, classe):
                self.transicoes[c] = classe



        classesEquiv = [self.estados.difference(self.estadosFinais), self.estadosFinais]



    def minimizar(self):
        self.eliminarInalcancaveis()
        self.eliminarMortos()
        self.reduzirParaEquivalencia()

# ======= Printar no terminal =========

    def printar(self):
        estados = list(self.estados)
        estados.sort() 
        alfabeto = list(self.alfabeto)
        alfabeto.sort() 
        # header
        linhas = []
        l = "    "
        l2 = "----"
        for c in alfabeto:
            l += (" | " + c + " ")
            l2 += "-|---"
        linhas.append(l)
        linhas.append(l2)
        # cada estado
        for estado in estados:
            l = ""
            # estado inicial
            if estado == self.estadoInicial:
                l += "->"
            else:
                l += "  "
            # estado inicial
            if estado in self.estadosFinais:
                l += "*"
            else:
                l += " "
            l += str(estado)
            # cada letra do alfabeto
            for c in alfabeto:
                if estado in self.transicoes and c in self.transicoes[estado]:
                    l += " | " + str(self.transicoes[estado][c])
                else:
                    l += " | -"
            l += " "
            linhas.append(l)
        # deixar bonitinho no terminal
        tamanho = [len(l) for l in linhas]
        maiorLinha = linhas[tamanho.index(max(tamanho))]
        tamEntreBarras = [len(i) for i in maiorLinha.split('|')] + [0]
        for linha in linhas:
            linha_out = ""
            linha_split = linha.split('|')
            for i in range(len(linha_split)):
                secao = linha_split[i]
                # para cada character a menos antes da barra
                espacos = tamEntreBarras[i] - len(secao)
                linha_out += secao + (" " * espacos) + '|'

            print(linha_out)
