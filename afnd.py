from afd import *

class AFND(AFD):

    def __init__(self, estados, alfabeto, estadoInicial, estadosFinais, transicoes=None):
        super().__init__(estados, alfabeto, estadoInicial, estadosFinais, transicoes)
        self.alfabeto.add("&")

        self.epsilonFecho = {}



    def epsilonFechoFunc(self, estado):
        self.epsilonFecho[estado] = set([estado])
        current = [estado]
        visited = set()

        while len(current)>0:
            next = []
            for s in current:
                if '&' in self.transicoes[s]:
                    for t in self.transicoes[s]['&']:
                        if not t in visited:
                            next.append(t)
                            visited.append(t)
                        self.epsilonFecho[estado].add(t)
            current = next
        return


    def computar(self, s):
        for t in self.estados:
            self.epsilonFechoFunc(t)

        estadosAtuais = self.epsilonFecho[self.estadoInicial]

        for c in s:
            if c not in self.alfabeto:
                raise SimboloInexistente(str(c))

            proximosEstados = set()

            for e in estadosAtuais:
                if c in self.transicoes[e]:
                    print(self.epsilonFecho)
                    print(self.transicoes[e][c])
                    t = map(lambda x: self.epsilonFecho[x], \
                                            self.transicoes[e][c])
                    alguma = []
                    for i in t:
                        for _ in range(len(i)):
                            alguma.append(i.pop())
                    proximosEstados.union(set(alguma))

            estadosAtuais = proximosEstados

        for e in estadosAtuais:
            if e in self.estadosFinais:
                return True
        return False
