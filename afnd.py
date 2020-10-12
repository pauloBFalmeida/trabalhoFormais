from afd import *

class AFND(AFD):

    def __init__(self, estados, alfabeto, estadoInicial, estadosFinais, transicoes=None):
        super().__init__(estados, alfabeto, estadoInicial, estadosFinais, transicoes)
        self.alfabeto.add("&")

    #    self.epsilonFecho = {}

    #def epsilonFechoFunc(self, estado):
    #    self.epsilonFecho[estado] = set([estado])
    #    current = [estado]
    #    visited = set()

    #    while len(current)>0:
    #        next = []
    #        for s in current:
    #            if '&' in self.transicoes[s]:
    #                for t in self.transicoes[s]['&']:
    #                    if not t in visited:
    #                        next.append(t)
    #                        visited.append(t)
    #                    self.epsilonFecho[estado].add(t)
    #        current = next
    #    return

    def computar(self, s):
        estadosAtuais = set([self.estadoInicial])
        for c in s:
            # simbolo nao pertecente ao alfabeto
            if c not in self.alfabeto:
                raise SimboloInexistente(str(c))
            for ea in estadosAtuais:
                # passo pelas epsilon transicoes
                if '&' in self.transicoes[ea]:
                    estadosAtuais.add(self.transicoes[ea]['&'])
                # removo os estados com transicoes mortas
                if c not in self.transicoes[ea]:
                    estadosAtuais.remove(ea)
            # nenhum estado restante com trasicoes validas
            if len(estadosAtuais) == 0:
                return False
            # percorro as transicoes
            estados = list(estadosAtuais)
            estadosAtuais.clear()
            for ea in estados:
                estadosAtuais.update([ne for ne in self.transicoes[ea][c]])
        # vejo se tem algum estado que seja de aceitacao
        for ea in estadosAtuais:
            if ea in self.estadosFinais:
                return True
        return False

