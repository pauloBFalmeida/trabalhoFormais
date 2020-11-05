from erros import *
# from afd import *
# from afnd import *

class GR():

# ======= Criacao =========

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

# ======= Derivacao =========

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

# ======= Conversao para AFND =========

    def converterParaAFND(self):
        from afnd import AFND
        # simbolo '#' representa o estado final
        automato = AFND(self.naoTerminais.union(set('#')),
                        self.terminais,
                        self.simboloInicial,
                        ["#"])
        # adiciono as transicoes no AF
        for simbolo in self.producoes:
            for prod in self.producoes[simbolo]:
                if len(prod) == 1:
                    automato.addTransicao(simbolo, prod[0], '#')
                else:
                    automato.addTransicao(simbolo, prod[0], prod[1])
        # ajusto os nomes e retorno o automato
        return automato
    
# ======= Print no terminal =========

    def printar(self):
        simbolosNaoIniciais = [p for p in self.producoes if p != self.simboloInicial]
        for simbolo in [self.simboloInicial] + simbolosNaoIniciais:
            l = simbolo + " -> "
            for prod in self.producoes[simbolo]:
                l += prod + " | "
            print(l[:-2])

# ======= Exportar para Arquivo =========

    def exportarParaArquivo(self, nomeArquivo):
        texto = ""
        # producoes
        for simbolo in self.producoes:
            texto += simbolo + " -> "
            for derivacao in self.producoes[simbolo]:
                texto += derivacao + " |"
            texto = texto[:-2] + '\n'
        # escrever no arquivo
        with open(nomeArquivo, 'w') as arquivo:
            arquivo.write(texto)


