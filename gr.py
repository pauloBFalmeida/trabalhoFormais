from erros import *
# from afd import *
# from afnd import *

class GR():

    def __init__(self, simboloInicial='S', terminais=[], naoTerminais=[]):
        self.simboloInicial = simboloInicial
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
        self.passoDerivacao([self.simboloInicial], profundidadeMax)

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

    def converterParaAFND(self):
        from afnd import AFND
        # representa o estado final
        automato = AFND(self.naoTerminais.union(set('#')),
                        self.terminais,
                        self.simboloInicial,
                        ["#"])

        for simbolo in self.producoes:
            for prod in self.producoes[simbolo]:
                if len(prod) == 1:
                    automato.addTransicao(simbolo, prod[0], '#')
                else:
                    automato.addTransicao(simbolo, prod[0], prod[1])

        return automato

    def printar(self):
        l = self.simboloInicial + " -> "
        for prod in self.producoes[self.simboloInicial]:
            l += prod + " | "
        print(l[:-2])
        for simbolo in self.producoes:
            if simbolo != self.simboloInicial:
                l = simbolo + " -> "
                for prod in self.producoes[simbolo]:
                    l += prod + " | "
                print(l[:-2])
