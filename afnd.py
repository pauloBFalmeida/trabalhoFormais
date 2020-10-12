import afd

class AFND(AFD):

    def __init__(self, estados, alfabeto, estadoInicial, estadosFinais, transicoes=None):
        super().__init__(estados, alfabeto, estadoInicial, estadosFinais, transicoes)
        self.alfabeto.add("&")

        self.epsilonFecho = {}



    def epsilonFecho(self, estado):
        self.epsilonFecho[estado] = set()
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
            self.epsilonFecho(t)

        estadosAtuais = epsilonFecho(estadoInicial)

        for c in s:
            if c not in self.alfabeto:
                raise SimboloInexistente(str(c))

            proximosEstados = set()

            for e in estadosAtuais:
                if c in self.transicoes[e]:
                    proximosEstados.union(set(map(lambda x: self.epsilonFecho[x], \
                                                  self.transicoes[e][c])))

            estadosAtuais = proximosEstados

        for e in estadosAtuais:
            if e in estadosFinais:
                return True
        return False
