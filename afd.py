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

        # novasTransicoes = {}
        transicoes = self.transicoes
        self.transicoes =  {}

        for estado in transicoes:
            for c in transicoes[estado]:
                for s in transicoes[estado][c]:
                    if estado in produtivos and s in produtivos:
                        self.addTransicao(estado, c, s)




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

        # novasTransicoes = {}
        transicoes = self.transicoes
        self.transicoes = {}

        for estado in transicoes:
            for c in transicoes[estado]:
                for s in transicoes[estado][c]:
                    if estado in visited and s in visited:
                        self.addTransicao(estado, c, s)

        # self.transicoes = novasTransicoes


    def reduzirParaEquivalencia(self):
        class Equivalencia():
            def __init__(self, estado):
                self.estado = estado
                self.classe_index = None
                self.transicoes = {}
            def setClasse(self, classe_index):
                self.classe_index = classe_index
            def addTransicao(self, c, classe):
                self.transicoes[c] = classe

        refs = {}
        for e in self.estados:
            refs[e] = Equivalencia(e)
            if e in self.estadosFinais:
                refs[e].classe_index = 1
            else:
                refs[e].classe_index = 0
        for i in self.estados:
            print(i)
        print("rdjsaiodjasijdisaj")

        classesEquiv = [self.estados.difference(self.estadosFinais), self.estadosFinais]

        done = False
        while not done:
            done = True
            for c in self.alfabeto:
                for classe in classesEquiv.copy():
                    primeiro = True
                    classe_apontada = None
                    nova_classe = set()
                    # print("character = " + c)
                    for elem in classe:
                        primeiro = True
                        classe_apontada_primeiro = None
                        nova_classe = set()
                        for elem in classe:
                            classe_apontada = None
                            if elem in self.transicoes and c in self.transicoes[elem]:
                                classe_apontada = refs[list(self.transicoes[elem][c])[0]].classe_index
                            if primeiro:
                                primeiro = False
                                classe_apontada_primeiro = classe_apontada
                            elif classe_apontada != classe_apontada_primeiro:
                                nova_classe.add(elem)
                                done = False
                    if len(nova_classe) > 0:
                        classesEquiv.append(nova_classe)
                        print(classesEquiv)
                        index = -1
                        for e in nova_classe:
                            index = refs[e].classe_index
                            break
                        classesEquiv[index] = classesEquiv[index].difference(nova_classe)
                        for e in nova_classe:
                            refs[e].classe_index = len(classesEquiv) - 1
        # print(classesEquiv)
        print(classesEquiv)
        estados = []
        estadosFinais = []
        for classe in classesEquiv:
            for e in classe:
                if e in self.estadosFinais:
                    estadosFinais.append(e)
                estados.append(e)
                break

        estadoInicial = [e for e in classesEquiv[refs[self.estadoInicial].classe_index]][0]

        # estadosFinais = []

        self.estados = set(estados)
        self.estadoInicial = estadoInicial
        self.estadosFinais = set(estadosFinais)

        transicoes = self.transicoes
        self.transicoes = {}

        for e in estados:
            for c in self.alfabeto:
                if e in transicoes and c in transicoes[e]:
                    self.addTransicao(e, c, estados[refs[list(transicoes[e][c])[0]].classe_index])


    def minimizar(self):
        print(self.estados)
        self.eliminarInalcancaveis()
        self.printar()
        self.eliminarMortos()
        self.printar()
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
            linhas.append(l.replace("{", "").replace("}", "").replace("\'", ""))
        # tamanho de chars de cada coluna
        tamEntreBarras = []
        linhasSplit = [i.split("|") for i in linhas]
        for i in range(len(linhasSplit[0])):
            maior = max([len(l[i]) for l in linhasSplit])
            tamEntreBarras.append(maior)
        # deixar bonitinho no terminal
        for linha in linhas:
            linha_out = ""
            linha_split = linha.split('|')
            for i in range(len(linha_split)):
                secao = linha_split[i]
                # para cada character a menos antes da barra
                espacos = tamEntreBarras[i] - len(secao)
                linha_out += secao + (" " * espacos) + '|'

            print(linha_out)
