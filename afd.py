# -*- coding: utf-8 -*-
from erros import *
from gr import *

class AFD():

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
                    e_prox = e #'-'
                    i_prox = i #'-'
                    if c not in self.transicoes[e] or c not in automato.transicoes[i]:
                        continue
                    if c in self.transicoes[e]:
                        e_prox = list(self.transicoes[e][c])[0]
                    if c in automato.transicoes[i]:
                        i_prox = list(automato.transicoes[i][c])[0]
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
                    e_prox = e #'-'
                    i_prox = i #'-'
                    if c not in self.transicoes[e] or c not in automato.transicoes[i]:
                        continue
                    if c in self.transicoes[e]:
                        e_prox = list(self.transicoes[e][c])[0]
                    if c in automato.transicoes[i]:
                        i_prox = list(automato.transicoes[i][c])[0]
                    estado_atual =  e +' & '+ i
                    estado_prox = e_prox +' & '+ i_prox
                    afdInterseccao.addTransicao(estado_atual, c, estado_prox)

        return afdInterseccao


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

    def converterParaGR(self):
        gramatica = GR(self.estadoInicial, list(self.alfabeto), list(self.estados))

        for estado in self.transicoes:
            for c in self.transicoes[estado]:
                gramatica.addProducao(str(estado), c + str(list(self.transicoes[estado][c])[0]))
                if list(self.transicoes[estado][c])[0] in self.estadosFinais:
                    gramatica.addProducao(str(estado), c)
        return gramatica

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
        i = 2

        classes = [self.estadosFinais, self.estados.difference(self.estadosFinais)]

        def getClasse(estado):
            for i in range(len(classes)):
                if estado in classes[i]:
                    print("RETURNING")
                    print(i)
                    print(classes[i])
                    return i
            raise ZeroDivisionError

        # falta considerar se a classe inteira transitar pro vazio

        while True:
            new_classes = []
            classeCriada = False
            for classe in classes:
                print(classe)
                new_class = set()
                for c in self.alfabeto:
                    for e in classe:
                        print(list(self.transicoes[min(classe)][c]))
                        if e == min(classe):
                            continue
                        if e not in self.transicoes or c not in self.transicoes[e] or \
                            min(classe) not in self.transicoes or c not in self.transicoes[min(classe)] or \
                            len(self.transicoes[e][c]) != len(self.transicoes[min(classe)][c]) or \
                            getClasse(list(self.transicoes[e][c])[0]) != getClasse(list(self.transicoes[min(classe)][c])[0]):
                            classeCriada = True
                            new_class.add(e)

                new_classes.append(new_class)
            for i in range(len(classes)):
                for j in range(len(new_classes)):
                    if len(new_classes[j]) == 0:
                        continue
                    print("iodsajiodsa")
                    print(classes[i])
                    print(new_classes[j])
                    print()
                    classes[i] = classes[i].intersection(new_classes[j])
            classes = classes + new_classes
            if not classeCriada:
                break

        print(classes)


    def minimizar(self):
        self.eliminarInalcancaveis()
        self.eliminarMortos()
        self.reduzirParaEquivalencia()


    def printar(self):

        l = "    "
        for c in self.alfabeto:
            l += (" | " + c + " ")
        l += " |"
        print(l)
        for estado in self.estados:
            l = ""
            if estado == self.estadoInicial:
                l += "->"
            else:
                l += "  "
            if estado in self.estadosFinais:
                l += "*"
            else:
                l += " "
            l += str(estado)
            for c in self.alfabeto:
                if estado in self.transicoes and c in self.transicoes[estado]:
                    l += " | " + str(self.transicoes[estado][c])
                else:
                    l += " | -"
            l += " |"
            print(l)
