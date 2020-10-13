from erros import *

class GR():

    def __init__(self, estadoInicial='S', terminais=[], naoTerminais=[]):
        self.estadoInicial = estadoInicial
        self.terminais = set(terminais)
        self.naoTerminais = set(naoTerminais)
        self.producoes = {}

    def addTerminal(self, a):
        self.terminais.add(a)


    def addNaoTerminal(self, a):
        self.naoTerminais.add(a)


    def addProducao(self, simbolo, derivacao):
        if (len(derivacao) == 1 and derivacao not in self.terminais) or \
           (len(derivacao) == 2 and (derivacao[0] not in self.terminais or derivacao[1] not in self.naoTerminais) or \
           (len(derivacao) > 2)) or \
           (len(simbolo) != 1 or simbolo not in self.naoTerminais):
            raise GramaticaNaoRegular()
        if simbolo not in self.producoes:
            self.producoes[simbolo] = set()
        self.producoes[simbolo].add(derivacao)

    def derivar(self, profundidadeMax):
        self.passoDerivacao(['S'], profundidadeMax)

    def passoDerivacao(self, cadeia, nivel):

        if nivel == 0:
            for c in cadeia:
                if c not in self.terminais:
                    return
            print(''.join(cadeia))
            return

        for i in range(len(cadeia)):
            s = cadeia[i]
            if s in self.naoTerminais and s in self.producoes:
                prods = self.producoes[s]
                for prod in prods:
                    prod = list(prod)
                    cadeia = cadeia[:i] + prod + cadeia[i+len(prod):]
                    self.passoDerivacao(cadeia, nivel-1)
                    cadeia = cadeia[:i] + [s] + cadeia[i+len(prod):]
