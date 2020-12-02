
from erros import *

class GLC():


    def __init__(self, simboloInicial='S', terminais=[], naoTerminais=[]):
        self.simboloInicial = simboloInicial
        self.terminais = set(terminais).union({'&'})
        self.naoTerminais = set(naoTerminais)
        self.producoes = {}

        self.firsts = {}
        self.follows = {}
        self.tabela = {}

    def setSimboloInicial(self, s):
        self.simboloInicial = s

    # ------- adicionar -------

    def addTerminal(self, a):
        self.terminais.add(a)

    def addNaoTerminal(self, a):
        self.naoTerminais.add(a)

    def addProducao(self, simbolo, derivacao):
        if simbolo not in self.naoTerminais:
            raise SimboloInexistente(simbolo)
        for c in derivacao:
            if c not in self.naoTerminais and c not in self.terminais:
                raise SimboloInexistente(c)
        # adiciona a producao
        if simbolo not in self.producoes:
            self.producoes[simbolo] = set()
        self.producoes[simbolo].add(tuple(derivacao))

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

# ========== Remover Inuteis =========

    def removerInuteis(self):
        while True:
            p1 = self.removerInalcancaveis()
            p2 = self.removerImprodutivos()
            # p2 = False
            # p1 = False
            if (not p1) and (not p2):
                break

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

# ======== Remover Epsilon Producoes ==============

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
                if deriv[0] == "&":
                    continue
                permutacoes = set(perms(deriv))
                if "" in permutacoes:
                    permutacoes.discard("")
                novasDerivacoes = novasDerivacoes.union(permutacoes)

            novasProducoes[s] = novasDerivacoes

        if self.simboloInicial in anulaveis:
            novasProducoes["S'"] = {tuple(self.simboloInicial), tuple("&")}
            self.simboloInicial = "S'"
            self.naoTerminais.add("S'")
        self.producoes = novasProducoes

# ========= Forma Normal de Chomsky ==========

    def formaNormalChomsky(self):
        self.removerEpsilonProd()
        self.remProdUnitarias()
        self.removerInuteis()
        # troca os terminais por nao terminais
        producoes = self.producoes
        self.producoes = {}
        tParaNT = {}
        for s in producoes:
            for prod in producoes[s]:
                if len(prod) == 1:
                    self.addProducao(s, prod)
                if len(prod) >= 2:
                    novaProd = []
                    for c in prod:
                        if c in self.terminais:
                            if c not in tParaNT:
                                tParaNT[c] = c.upper()+"#"
                                self.naoTerminais.add(tParaNT[c])
                            novaProd.append(tParaNT[c])
                        else:
                            novaProd.append(c)
                    self.addProducao(s, novaProd)
        for t in tParaNT:
            self.naoTerminais.add(tParaNT[t])
            self.producoes[tParaNT[t]] = t
        # quebra as producoes com mais de 2 nao terminais
        producoes = self.producoes
        self.producoes = {}
        for s in producoes:
            contador = 1
            for prod in producoes[s]:
                if len(prod) > 2:
                    novaNT1 = s
                    for nt in prod[:-2]:
                        novaNT2 = s + str(contador)
                        self.naoTerminais.add(novaNT2)
                        self.addProducao(novaNT1, [nt, novaNT2])
                        novaNT1 = novaNT2
                        contador += 1
                    self.addProducao(novaNT2, [prod[-2], prod[-1]])
                else:
                    self.addProducao(s, prod)


    def remProdUnitarias(self):
        conjN = {}
        for s in self.naoTerminais:
            conjN[s] = set([s])
            if s in self.producoes:
                for deriv in self.producoes[s]:
                    if len(deriv) == 1 and deriv[0] in self.naoTerminais:
                        conjN[s].add(deriv[0])
        #
        mudou = True
        while mudou:
            mudou = False
            for s in self.producoes:
                novo = conjN[s]
                for k in conjN[s]:
                    novo = novo.union(conjN[k])
                if len(novo) > len(conjN[s]):
                    conjN[s] = novo
                    mudou = True
        #
        producoes = self.producoes
        self.producoes = {}
        # para cada nao terminal pego as producoes nao unitarias
        for s in producoes:
            for prod in [p for p in producoes[s] if not (len(p) == 1 and p[0] in self.naoTerminais)]:
                # para todos os NT com 's' no conjN
                for k in conjN:
                    if s in conjN[k]:
                        # add producoes
                        if k not in self.producoes:
                            self.producoes[k] = set()
                        self.producoes[k].add(prod)


# ========= Recursao a Esquerda =============


    def remRecEsq(self):
        producoes = {}

        for p in self.producoes:
            producoes[p] = self.producoes[p].copy()

        # remover producoes circular
        for s in self.producoes:
            for prod in self.producoes[s].copy():
                if prod == tuple(s):
                    producoes[s].discard(prod)

        #
        self.producoes = {}
        for p in producoes:
            self.producoes[p] = producoes[p].copy()

        # for p in self.producoes:
        #     producoes[p] = self.producoes[p].copy()
        # producoes = self.producoes.copy()

        keys = list(producoes.keys())
        print(keys)
        counter = -1
        for i in keys:
            counter+=1
            for j in keys[:counter]:
                for prodi in producoes[i]:
                    # remove producao (n a adicionamos nas novas producoes)
                    if j == prodi[0]:
                        self.remProducao(i, prodi)
                        for prodj in producoes[j]:
                            if prodj != tuple('&'):
                                self.addProducao(i, prodj+prodi[1:])
                            else:
                                self.addProducao(i, prodi[1:])
                producoes[i] = self.producoes[i].copy()
            #

            recursivos = []
            naoRec = []
            for prod in self.producoes[i]:
                if prod[0] == i:
                    recursivos.append(prod[1:])
                else:
                    naoRec.append(prod)
            if len(recursivos) > 0:
                ia = i+"@"
                self.naoTerminais.add(ia)
                novasProdI  = set()
                novasProdIa = set(tuple("&"))
                for r in recursivos:
                    novasProdIa.add(r+tuple(ia))
                for n in naoRec:
                    novasProdI.add(n+tuple(ia))
                self.producoes[i]  = novasProdI
                self.producoes[ia] = novasProdIa

# ======== Fatoracao ========

    def fatoracao(self, profundidade=10):
        while profundidade > 0 and self.remNDetIndireto():
            profundidade -= 1


    def remNDetIndireto(self):
        haMudanca = False
        for s in self.producoes:
            self.calcfirsts(s)
        # encontrar producoes que levam ao nao determinismo
        for s in self.producoes:
            auxiliar = []
            problematicas = set()
            for prod in self.producoes[s]:
                firsts = self.calcFirstsCadeia(prod)
                # interseccao com o firsts de uma aux
                for a in auxiliar:
                    if len(firsts.intersection(a[1])) > 0:
                        problematicas.add(prod)
                        problematicas.add(a[0])
                        haMudanca = True
                #
                for i in range(len(prod)-1):
                    c = prod[i]
                    #print(c)
                    #print(self.firsts[c])
                    #print('&' in self.firsts[c])
                    #print(len(self.firsts[c].intersection(self.calcFirstsCadeia(prod[i+1:]))) > 0)
                    if c in self.naoTerminais and '&' in self.firsts[c] and \
                            len(self.firsts[c].intersection(self.calcFirstsCadeia(prod[i+1:]))) > 0:
                        problematicas.add(prod)
                        #print(c+'dentro do if')
                        haMudanca = True
                #
                auxiliar.append( (prod, firsts) )
            #
            for prod in problematicas:
                self.producoes[s].discard(prod)
            #
            for prod in problematicas:
                derivacoes = self.derivar(prod)
                if tuple() in derivacoes:
                    derivacoes.remove(tuple())
                    derivacoes.append(tuple('&'))
                for d in derivacoes:
                    nt = ''.join(s)
                    self.naoTerminais.add(nt)
                    self.addProducao(nt, d)
        #
        self.remNDetDireto()
        return haMudanca


    def derivar(self, entrada):
        if len(entrada) == 0:
            return [tuple()]
        if entrada[0] in self.terminais:
            return [entrada[0] + ''.join(prod) for prod in self.derivar(entrada[1:])]
        elif entrada[0] in self.producoes:
            saida = []
            derivacoes = self.derivar(entrada[1:])
            for prod in self.producoes[entrada[0]]:
                if prod == tuple('&'):
                    saida += derivacoes
                else:
                    saida += [''.join(prod) + ''.join(deriv) for deriv in derivacoes]
            return saida

    def remNDetDireto(self):

        producoes = self.producoes
        self.producoes = {}
        for s in producoes.copy():
            auxiliar = []
            for prod in producoes[s].copy():
                if len(auxiliar) == 0:
                    auxiliar.append(prod)
                    continue
                #
                encontrouPref = False
                for i in range(len(auxiliar)):
                    prodA = auxiliar[i]
                    # maior prefixo
                    maxPref = []
                    j = 0
                    while prod[j] == prodA[j]:
                        maxPref.append(prod[j])
                        j += 1
                        if j >= min(len(prod), len(prodA)):
                            break
                    if len(maxPref) > 0:
                        auxiliar[i] = tuple(maxPref)
                        encontrouPref = True
                #
                if not encontrouPref:
                    auxiliar.append(prod)
            #
            contador = 1
            for aux in auxiliar:
                producoesAux = []
                for prod in producoes[s]:
                    if len(aux) <= len(prod) and aux == prod[:len(aux)]:
                        producoesAux.append(prod)
                if len(producoesAux) > 1:
                    nt = s +'!'+ str(contador)
                    self.naoTerminais.add(nt)
                    contador += 1
                    #
                    self.addProducao(s, aux+ (nt,) )
                    for p in producoesAux:
                        p = p[len(aux):]
                        p = p if len(p) > 0 else tuple('&')
                        self.addProducao(nt, p)
                else:
                    self.addProducao(s, aux)


# ======== reconhecedor ========

    def analisar(self, sentenca):
        self.construirAnalisador()
        sentenca = sentenca + '$'
        cabecote = 0
        pilha = ['$']

        pilha.append(self.simboloInicial)

        while True:

            print()
            print(sentenca[cabecote:])
            print(pilha)

            topo = pilha[-1]
            s = sentenca[cabecote]

            if topo == "&":
                pilha.pop()
                continue

            if topo == "$" and s == "$":
                return True
            elif topo in self.terminais and topo == s:
                print("desempilha")
                pilha.pop()
                cabecote += 1
            else:
                if (topo, s) in self.tabela:
                    prod = list(self.tabela[(topo, s)])
                    print("producao: " + str(prod))
                    prod.reverse()
                    pilha.pop()
                    for i in prod:
                        pilha.append(i)
                else:
                    return False

    def calcfirsts(self, c):
        if c in self.firsts:
            return self.firsts[c].copy()

        if c in self.terminais:
            self.firsts[c] = set(c)
            return set(c)

        firstc = set()
        if c in self.producoes:
            for prod in self.producoes[c]:
                if prod[0] in self.terminais:
                    # print(f'{c} adic {prod[0]}')
                    firstc.add(prod[0])
                elif prod == '&':
                    # print(f'{c} !!!!!')
                    firstc.add('&')
                else:
                    soEpsilons = True
                    for nt in prod:
                        cf = self.calcfirsts(nt)
                        if '&' in cf:
                            cf.discard('&')
                        firstc = firstc.union(cf)
                        # print(f'first {c} <- {cf}')
                        # print(f'{firstc}')
                        # print(('&' not in self.firsts[nt]))
                        if '&' not in self.firsts[nt]:
                            soEpsilons = False
                            break
                    if soEpsilons:
                        # print(f'para {c} adiciona &')
                        firstc.add('&')
        self.firsts[c] = firstc
        return firstc.copy()

    def calcFirstsCadeia(self, cadeia):

        firstc = set()
        soEpsilons = True
        for nt in cadeia:
            cf = self.calcfirsts(nt)
            if '&' in cf:
                cf.discard('&')
            firstc = firstc.union(cf)
            if '&' not in self.firsts[nt]:
                soEpsilons = False
                break
        if soEpsilons:
            firstc.add('&')
        return firstc

    def calcfollows1(self):

        for c in self.naoTerminais:
            # followc = set()
            if c in self.producoes:
                if c not in self.follows:
                    self.follows[c] = set()
                for prod in self.producoes[c]:

                    for i in range(len(prod)-1):
                        atual = prod[i]
                        if atual in self.terminais:
                            continue

                        if atual not in self.follows:
                            self.follows[atual] = set()
                        print(f'para {prod[i+1:]} = {self.calcFirstsCadeia(prod[i+1:])}')
                        self.follows[atual] = self.follows[atual].union(self.calcFirstsCadeia(prod[i+1:]))
                        if '&' in self.follows[atual]:
                            self.follows[atual].discard('&')
        return

    def calcfollows2(self):
        haMudanca = False
        for c in self.naoTerminais:
            # followc = set()
            if c in self.producoes:
                for prod in self.producoes[c]:

                    for i in range(len(prod)):
                        atual = prod[i]
                        if atual in self.terminais:
                            continue
                        if atual not in self.follows:
                            self.follows[atual] = set()

                        if i == len(prod)-1:
                            l = len(self.follows[atual])
                            self.follows[atual] = self.follows[atual].union(self.follows[c])
                            if (len(self.follows[atual]) > l):
                                haMudanca = True
                            continue
                        if '&' in self.calcFirstsCadeia(prod[i+1:]):
                            l = len(self.follows[atual])
                            self.follows[atual] = self.follows[atual].union(self.follows[c])
                            if (len(self.follows[atual]) > l):
                                haMudanca = True
        return haMudanca

    def construirTabela(self):
        self.tabela = {}

        for s in self.naoTerminais:
            if s in self.producoes:
                for prod in self.producoes[s]:
                    pf = self.calcFirstsCadeia(prod)

                    if '&' in pf:
                        for t in self.follows[s]:
                            self.tabela[(s, t)] = prod

                    pf.discard('&')

                    for t in pf:
                        self.tabela[(s, t)] = prod


    def construirAnalisador(self):
        self.remRecEsq()
        self.fatorar()
        for s in self.naoTerminais:
            self.calcfirsts(s)

        self.follows[self.simboloInicial] = set('$')

        self.calcfollows1()
        while self.calcfollows2(): pass

        print("FIRSTS")
        for f in self.firsts:
            print(f'{f} -> {self.firsts[f]}')

        print("Follows")
        for f in self.follows:
            print(f'{f} -> {self.follows[f]}')

        for s in self.naoTerminais:
            if len(self.firsts[s].intersection(self.follows[s])) != 0:
                print("Linguagem não pode ser parseada com LL(1)")
                return

        self.construirTabela()

        for t in self.tabela:
            print(f'{t} -> {self.tabela[t]}')


# ======= ajustar Nome Producoes =========

    def ajustarNomeProducoes(self):
        nomesNT = {self.simboloInicial: 'S'}
        # ajustar os nomes
        contadorNT = {}
        naoTerminais = set()
        for s in self.naoTerminais:
            nt = s[0]
            if len(s) > 1 and s[1] in ['!','@',"'"]:
                nt += s[1]
            if nt not in contadorNT:
                contadorNT[nt] = 0
            else:
                contadorNT[nt] += 1
                nt = nt + str(contadorNT[nt])
            #
            naoTerminais.add(nt)
            nomesNT[s] = nt

        # ajustar as producoes
        self.naoTerminais = naoTerminais
        producoes = self.producoes
        self.producoes = {}
        for s in producoes:
            for prod in producoes[s]:
                novaProd = []
                for p in prod:
                    if p in nomesNT:
                        novaProd.append(nomesNT[p])
                    else:
                        novaProd.append(p)
                # adiciona a nova prod
                self.addProducao(nomesNT[s], novaProd)

# ======= printar ===========

    def printar(self):
        simbolosNaoIniciais = [p for p in self.producoes if p != self.simboloInicial]
        simbolosNaoIniciais.sort()
        for simbolo in [self.simboloInicial] + simbolosNaoIniciais:
            l = simbolo + " -> "
            for prod in self.producoes[simbolo]:
                l += "".join(prod) + " | "
            print(l[:-2])

# ======= Exportar para Arquivo =========

    def exportarParaArquivo(self, nomeArquivo):
        texto = ""
        # producoes
        for simbolo in [self.simboloInicial] + [p for p in self.producoes if p != self.simboloInicial]:
            texto += simbolo + " -> "
            for derivacao in self.producoes[simbolo]:
                texto += ''.join(derivacao) + " | "
            texto = texto[:-3] + '\n'
        # escrever no arquivo
        with open(nomeArquivo, 'w') as arquivo:
            arquivo.write(texto)
