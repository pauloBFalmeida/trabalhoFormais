from afd import *

class AFND(AFD):

    def __init__(self, estados, alfabeto, estadoInicial, estadosFinais):
        super().__init__(estados, alfabeto, estadoInicial, estadosFinais)
        self.alfabeto.add("&")
        self.epsilonFechos = {}


    def epsilonFecho(self, estado):
        alcancaveis = set([estado])

        current = set()
        current.add(estado)
        visited = set()
        visited.add(estado)

        while len(current) > 0:
            next = set()

            for e in current:
                if e in self.transicoes and '&' in self.transicoes[e]:
                    for t in self.transicoes[e]['&']:
                        if t not in visited:
                            visited.add(t)
                            next.add(t)
            current = next

        return visited

    def gerarEpsilonFecho(self):
        for e in self.estados:
            self.epsilonFechos[e] = self.epsilonFecho(e)
        #for e in self.epsilonFechos:
        #    print(str(e) + " " + str(self.epsilonFechos[e]))

    def computar(self, s):
        self.gerarEpsilonFecho()

        estadoAtual = self.epsilonFecho[self.estadoInicial]

        for c in s:
            if c not in self.alfabeto:
                raise SimboloInexistente(str(c))

            proximoEstado = set()

            for e in estadoAtual:
                if e in self.transicoes and c in self.transicoes[e]:
                    for n in self.transicoes[e][c]:
                        proximoEstado = proximoEstado.union(self.epsilonFechos[n])

            estadoAtual = proximoEstado
        for e in estadoAtual:
            if e in self.estadosFinais:
                return True
        return False


    def traduzir(self, conjunto):
        k = 0
        for i in range(len(self.estados)):
            if i in conjunto or str(i) in conjunto:
                k = (k << 1) + 1
            else:
                k = k << 1
        return k

    def destraduzir(self, k):
        conjunto = set()
        for i in range(len(self.estados)-1, -1,-1):
            if k % 2 == 1:
                conjunto.add(i)
                k -= 1
            k = k >> 1
        return conjunto

    def printEstados(self):
        for t in self.transicoes:
            print(str(t)+' -> '+str(self.transicoes[t]))

    def determinizar(self):
        self.gerarEpsilonFecho()
        if '&' in self.alfabeto:
            self.alfabeto.remove('&')

        novasTransicoes = {}
        visitados = set()
        filaEstados = [self.epsilonFechos[self.estadoInicial]]

        while len(filaEstados) > 0:
            estadosAtuais = filaEstados.pop()
            visitados.add(self.traduzir(estadosAtuais))
            for c in self.alfabeto:
                estadosTransicao = set()
                for e in estadosAtuais:
                    if e in self.transicoes and c in self.transicoes[e]:
                        for p in self.transicoes[e][c]:
                            estadosTransicao.update(self.epsilonFechos[p])
                if len(estadosTransicao) > 0:
                    if self.traduzir(estadosAtuais) not in novasTransicoes:
                        novasTransicoes[self.traduzir(estadosAtuais)] = {}
                    novasTransicoes[self.traduzir(estadosAtuais)][c] = self.traduzir(estadosTransicao)
                    if self.traduzir(estadosTransicao) not in visitados:
                        filaEstados.append(estadosTransicao)

        print()
        for nt in novasTransicoes:
            print(str(nt)+' -> '+str(novasTransicoes[nt]))
            
        #afd = AFD()
        #return afd

        #self.__class__ = AFD
        #print(self.__class__)
        #print(self.alfabeto)
