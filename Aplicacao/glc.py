
from erros import *

class GLC():


    def __init__(self, simboloInicial='S', terminais=[], naoTerminais=[]):
        self.simboloInicial = simboloInicial
        self.terminais = set(terminais).union({'&'})
        self.naoTerminais = set(naoTerminais)
        self.producoes = {}

    def setSimboloInicial(self, s):
        self.simboloInicial = s

    # ------- adicionar -------

    def addTerminal(self, a):
        self.terminais.add(a)

    def addNaoTerminal(self, a):
        self.naoTerminais.add(a)

    def addProducao(self, simbolo, derivacao):
        # if (len(derivacao) == 1 and derivacao not in self.terminais) or \
        #    (len(derivacao) == 2 and (derivacao[0] not in self.terminais or derivacao[1] not in self.naoTerminais) or \
        #    (len(derivacao) > 2)) or \
        #    (len(simbolo) != 1 or simbolo not in self.naoTerminais):
        #     raise GramaticaNaoRegular()

        if simbolo not in self.naoTerminais:
            raise SimboloInexistente()

        for c in derivacao:
            if c not in self.naoTerminais and c not in self.terminais:
                raise SimboloInexistente()

        if simbolo not in self.producoes:
            self.producoes[simbolo] = set()
        self.producoes[simbolo].add(derivacao)

    # ------- remover -------

    def remTerminal(self, a):
        if a in self.terminais:
            self.terminais.discard(a)
            for e in self.producoes:
                aRemover = set()
                for d in self.producoes[e]:
                    if a in d:
                        aRemover.add(d)
                self.producoes[e] = self.producoes[e].difference(aRemover)

    def remNaoTerminal(self, s):
        if s in self.naoTerminais:
            self.naoTerminais.discard(s)
            del self.producoes[s]
            for e in self.producoes:
                aRemover = set()
                for d in self.producoes[e]:
                    if s in d:
                        aRemover.add(d)
                self.producoes[e] = self.producoes[e].difference(aRemover)

    def remProducao(self, esquerdo, direito):
        if esquerdo in self.producoes:
            if direito in self.producoes[esquerdo]:
                self.producoes[esquerdo].discard(direito)

    def removerImprodutivos(self):
        produtivos = self.terminais

        while True:
            q = set()
            for s in self.producoes:
                if s in produtivos:
                    continue
                for deriv in self.producoes[s]:
                    produtiva = True
                    for c in deriv:
                        if c not in produtivos:
                            produtiva = False
                    if produtiva:
                        q.add(s)
            if len(q) == 0:
                break
            produtivos = produtivos.union(q)

        novasProducoes = {}
        mudou = False

        for s in produtivos.difference(self.terminais):
            novasProducoes[s] = set()
            for deriv in self.producoes[s]:
                produtiva = True
                for c in deriv:
                    if c not in produtivos:
                        produtiva = False
                        mudou = True
                        break
                if produtiva:
                    novasProducoes[s].add(deriv)
        self.producoes = novasProducoes
        return mudou

    def removerInalcancaveis(self):
        alcancaveis = {self.simboloInicial}

        search = {self.simboloInicial}

        while True:
            q = set()
            # print(q)

            for s in search:
                if s not in self.producoes:
                    continue

                for deriv in self.producoes[s]:
                    for c in deriv:
                        if c in self.naoTerminais and c not in alcancaveis:
                            q.add(c)
            if len(q) == 0:
                break
            search = q
            alcancaveis = alcancaveis.union(q)

        if alcancaveis == self.naoTerminais:
            return False

        novasProducoes = {}
        mudou = False

        for s in self.producoes:
            if s in alcancaveis:
                novasProducoes[s] = set()

                if s in self.producoes:
                    for deriv in self.producoes[s]:
                        alcancavel =  True
                        for c in deriv:
                            if c in self.naoTerminais and c not in alcancaveis:
                                alcancavel = False
                                mudou = True
                                break
                        if alcancavel:
                            novasProducoes[s].add(deriv)
        self.producoes = novasProducoes
        return mudou

    def removerInuteis(self):
        while True:
            p1 = self.removerInalcancaveis()
            p2 = self.removerImprodutivos()
            # p2 = False
            # p1 = False
            if (not p1) and (not p2):
                break


    def removerEpsilonProd(self):

        anulaveis = {"&"}

        while True:
            q = set()
            for s in self.producoes:
                if s in anulaveis:
                    continue
                for deriv in self.producoes[s]:
                    anulavel = True
                    for c in deriv:
                        if c not in anulaveis:
                            anulavel = False
                    if anulavel:
                        q.add(s)
            if len(q) == 0:
                break
            anulaveis = anulaveis.union(q)

        def perms(deriv):
            if len(deriv) == 1:
                if deriv[0] in self.terminais:
                    return [deriv[0]]
                if deriv[0] not in anulaveis:
                    return [deriv[0]]
                return [deriv[0], ""]

            # print(deriv[1:])
            prods = perms(deriv[1:])
            print(deriv[0])
            if deriv[0] in self.terminais:
                # print([(deriv[0] + prod) for prod in prods])
                return [(deriv[0] + prod) for prod in prods]

            if deriv[0] not in anulaveis: # in naoTerminais
                # print([(deriv[0] + prod) for prod in prods])
                return [(deriv[0] + prod) for prod in prods]
            # print([(deriv[0] + prod) for prod in prods] +  [prod for prod in prods])
            return [(deriv[0] + prod) for prod in prods] +  [prod for prod in prods]

        novasProducoes = {}
        # print(anulaveis)
        # print(perms("ABC"))
        for s in self.producoes:

            novasDerivacoes = set()
            for deriv in self.producoes[s]:
                if deriv == "&":
                    continue
                permutacoes = set(perms(deriv))
                if "" in permutacoes:
                    permutacoes.discard("")
                novasDerivacoes = novasDerivacoes.union(permutacoes)

            novasProducoes[s] = novasDerivacoes

        if self.simboloInicial in anulaveis:
            novasProducoes["#"] = {self.simboloInicial, "&"}
        self.simboloInicial = "#"
        self.producoes = novasProducoes

    # def simbolosAEsquerda(self, simbolo, visited, trail):
    #     if simbolo in visited
    #
    # def encontrarRecsIndiretas(self):
    #
    #
    #
    #
    # def remRecEsq(self):



    def printar(self):
        simbolosNaoIniciais = [p for p in self.producoes if p != self.simboloInicial]
        simbolosNaoIniciais.sort()
        for simbolo in [self.simboloInicial] + simbolosNaoIniciais:
            l = simbolo + " -> "
            for prod in self.producoes[simbolo]:
                l += prod + " | "
            print(l[:-2])
