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

    def addTransicao(self, estadoInicial, simbolo, estadoProximo):
        if not estadoInicial in self.estados:
            raise EstadoInexistente(str(estadoInicial))
        if not estadoProximo in self.estados:
            raise EstadoInexistente(str(estadoProximo))
        if not simbolo in self.alfabeto:
            raise SimboloInexistente(str(simbolo))
        # se existir o estado, simbolo e proximo estado entao adiciono a transicao
        if not estadoInicial in self.transicoes:
            self.transicoes[estadoInicial] = {}
        if not simbolo in self.transicoes[estadoInicial]:
            self.transicoes[estadoInicial][simbolo] = set()
        self.transicoes[estadoInicial][simbolo].add(estadoProximo)

# ======= Uniao =========

    def uniao(self, automato):
        estados = []
        estadosFinais = []
        # cada estado da uniao eh dado pela uniao de cada estado nesse AF
        # com todos os estados do outro AF
        for e in self.estados:
            for i in automato.estados:
                estados.append(e + " & "  + i)
                # se um estado for final entao acrescento o estado da uniao nos finais
                if e in self.estadosFinais or i in automato.estadosFinais:
                    estadosFinais.append(e + " & " + i)
        # alfabeto e estado inicial sao unidos para criar o AFD da uniao
        alfabeto = self.alfabeto.union(automato.alfabeto)
        estadoInicial = (self.estadoInicial + " & " + automato.estadoInicial)
        afdUniao = AFD(estados, alfabeto, estadoInicial, estadosFinais)
        # para cada estado desse AF que tenha transicoes
        # pego cada estado do outro AF que tenha transicoes
        for e in self.estados:
            if e not in self.transicoes:
                continue
            for i in automato.estados:
                if i not in automato.transicoes:
                    continue
                # pego as transicoes para cada caracter do alfabeto
                for c in alfabeto:
                    e_prox = '-'
                    i_prox = '-'
                    if c in self.transicoes[e]:
                        e_prox = list(self.transicoes[e][c])[0]
                    if c in automato.transicoes[i]:
                        i_prox = list(automato.transicoes[i][c])[0]
                    # se ambos tiverem transicoes nao nulas, adiciono a transicao a uniao
                    if e_prox != '-' and i_prox != '-':
                        estado_atual =  e +' & '+ i
                        estado_prox = e_prox +' & '+ i_prox
                        afdUniao.addTransicao(estado_atual, c, estado_prox)
        # retorno o afd da uniao
        return afdUniao

# ======= Interseccao =========

    def interseccao(self, automato):
        estados = []
        estadosFinais = []
        # cada estado da uniao eh dado pela uniao de cada estado nesse AF
        # com todos os estados do outro AF
        for e in self.estados:
            for i in automato.estados:
                estados.append(e + " & "  + i)
                # se ambos estados forem finais entao acrescento o estado nos finais
                if e in self.estadosFinais and i in automato.estadosFinais:
                    estadosFinais.append(e + " & " + i)
        # alfabeto e estado inicial sao unidos para criar o AFD da interseccao
        alfabeto = self.alfabeto.union(automato.alfabeto)
        estadoInicial = (self.estadoInicial + " & " + automato.estadoInicial)
        afdInterseccao = AFD(estados, alfabeto, estadoInicial, estadosFinais)
        # para cada estado desse AF que tenha transicoes
        # pego cada estado do outro AF que tenha transicoes
        for e in self.estados:
            if e not in self.transicoes:
                continue
            for i in automato.estados:
                if i not in automato.transicoes:
                    continue
                # pego as transicoes para cada caracter do alfabeto
                for c in alfabeto:
                    e_prox = '-'
                    i_prox = '-'
                    if c in self.transicoes[e]:
                        e_prox = list(self.transicoes[e][c])[0]
                    if c in automato.transicoes[i]:
                        i_prox = list(automato.transicoes[i][c])[0]
                    # se ambos tiverem transicoes nao nulas, adiciono a transicao a uniao
                    if e_prox != '-' and i_prox != '-':
                        estado_atual =  e +' & '+ i
                        estado_prox = e_prox +' & '+ i_prox
                        afdInterseccao.addTransicao(estado_atual, c, estado_prox)
        # retorno o afd da interseccao
        return afdInterseccao

# ======= Computar entrada =========

    def computar(self, entrada):
        estadoAtual = self.estadoInicial
        # para cada caracter na entrada
        for c in entrada:
            if c not in self.alfabeto:
                raise SimboloInexistente(str(c))
            if c not in self.transicoes[estadoAtual]:
                raise TransicaoInexistente(str(estadoAtual), c)
            # avanco para o proximo estado pela transicao
            estadoAtual = list(self.transicoes[estadoAtual][c])[0]
        # se estiver nos estados finais aceito senao rejeito
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

        # atualizar transicoes
        transicoes = self.transicoes
        self.transicoes = {}
        for estado in transicoes:
            for c in transicoes[estado]:
                for s in transicoes[estado][c]:
                    if estado in visited and s in visited:
                        self.addTransicao(estado, c, s)


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

        classesEquiv = [self.estados.difference(self.estadosFinais), self.estadosFinais]

        done = False
        while not done:
            done = True
            for c in self.alfabeto:
                for classe in classesEquiv.copy():
                    primeiro = True
                    classe_apontada = None
                    nova_classe = set()
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
                        index = -1
                        for e in nova_classe:
                            index = refs[e].classe_index
                            break
                        classesEquiv[index] = classesEquiv[index].difference(nova_classe)
                        for e in nova_classe:
                            refs[e].classe_index = len(classesEquiv) - 1

        # ajustar estados
        estados = []
        estadosFinais = []
        for classe in classesEquiv:
            for e in classe:
                if e in self.estadosFinais:
                    estadosFinais.append(e)
                estados.append(e)
                break
            
        estadoInicial = [e for e in classesEquiv[refs[self.estadoInicial].classe_index]][0]
        # atualizar estados
        self.estados = set(estados)
        self.estadoInicial = estadoInicial
        self.estadosFinais = set(estadosFinais)
        # atualizar transicoes
        transicoes = self.transicoes
        self.transicoes = {}
        for e in transicoes:
            for c in transicoes[e]:
                for t in transicoes[e][c]:
                    self.addTransicao(e, c, estados[refs[t].classe_index])


    def minimizar(self):
        self.eliminarInalcancaveis()
        self.eliminarMortos()
        self.reduzirParaEquivalencia()

# ======= Ajustar estados e transicoes para numeros de [0..nEstados] =======

    def ajustarNomeEstados(self):
        # salvar antigos e zerar atributos
        estados = self.estados
        estadosFinais = self.estadosFinais
        estadoInicial = self.estadoInicial
        transicoes = self.transicoes
        self.estados = set()
        self.estadosFinais = set()
        self.estadoInicial = '0'
        self.transicoes = {}
        # linkar novo nome com estado
        nomeEstados = {estadoInicial: self.estadoInicial}
        for e in [e for e in estados if e != estadoInicial]:
            nomeEstados[e] = str(len(nomeEstados))
        # atualizar nome dos estados
        for e in estados:
            self.estados.add(nomeEstados[e])
            if e in estadosFinais:
                self.estadosFinais.add(nomeEstados[e])
        # mudar as transicoes
        for e in transicoes:
            for c in transicoes[e]:
                ne = nomeEstados[e]
                for t in transicoes[e][c]:
                    nt = nomeEstados[t]
                    self.addTransicao(ne, c, nt)

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
            l = l.translate(str.maketrans({'{': None, '}': None, "\'": None}))
            linhas.append(l)
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

# ======= Exportar para Arquivo =========
        
    def exportarParaArquivo(self, nomeArquivo):
        texto = ""
        # ajustar os estados para ficarem bonitinhos
        self.ajustarNomeEstados()
        # numero de estados
        texto += str(len(self.estados)) + '\n'
        # estado inicial
        texto += self.estadoInicial + '\n'
        # estados finais
        for e in self.estadosFinais:
            texto += e + ','
        texto = texto[:-1] + '\n'
        # alfabeto
        for c in self.alfabeto: 
            texto += str(c) + ','
        texto = texto[:-1] + '\n'
        # transições (uma por linha)
        for e in self.transicoes:
            for c in self.transicoes[e]:
                texto += e + ',' + c + ','
                for t in self.transicoes[e][c]:
                    texto += t + '-'
                texto = texto[:-1] + '\n'
        # escrever no arquivo
        with open(nomeArquivo, 'w') as arquivo:
            arquivo.write(texto)
