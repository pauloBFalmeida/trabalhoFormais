# -*- coding: utf-8 -*-
from erros import *

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
