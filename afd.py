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
