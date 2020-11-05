from afd import AFD

class AFND(AFD):

# ======= Criacao =========

    def __init__(self, estados, alfabeto, estadoInicial, estadosFinais):
        super().__init__(estados, alfabeto, estadoInicial, estadosFinais)
        self.alfabeto.add('&')
        self.epsilonFechos = {}

# ======= Epsilon Fecho =========

    def gerarEpsilonFecho(self):
        for e in self.estados:
            self.epsilonFechos[e] = self.epsilonFecho(e)

    def epsilonFecho(self, estado):
        alcancaveis = set([estado])
        current = set([estado])
        visited = set([estado])
        # enquanto ainda tiver mais estados nao visitados alcancaveis
        while len(current) > 0:
            next = set()
            # para cada estado pego o proximo estado alcancado pela 
            # epsilon transicao que nao foi visitado ainda
            for e in current:
                if e in self.transicoes and '&' in self.transicoes[e]:
                    for t in self.transicoes[e]['&']:
                        if t not in visited:
                            visited.add(t)
                            next.add(t)
            current = next
        return visited

# ======= Computar entrada =========

    def computar(self, entrada):
        self.gerarEpsilonFecho()
        estadoAtual = self.epsilonFecho[self.estadoInicial]
        # para cada caracter na entrada
        for c in entrada:
            if c not in self.alfabeto:
                raise SimboloInexistente(str(c))
            # gero o conjunto de estados alcancados pelas transicoes partindo dos estados atuais
            proximoEstado = set()
            for e in estadoAtual:
                if e in self.transicoes and c in self.transicoes[e]:
                    for n in self.transicoes[e][c]:
                        proximoEstado = proximoEstado.union(self.epsilonFechos[n])
            estadoAtual = proximoEstado
        # se estiver em pelo menos um estado finail aceito senao rejeito
        for e in estadoAtual:
            if e in self.estadosFinais:
                return True
        return False

# ======= Codificacao de conjunto de estados =========

    # codificacao 'binario' para um conjunto de estados
    def traduzir(self, conjunto):
        k = 0
        for i in range(len(self.estados)):
            if i in conjunto or str(i) in conjunto:
                k = (k << 1) + 1
            else:
                k = k << 1
        return str(k)
    
    # conjunto de estados especificados pela codificacao
    def destraduzir(self, k):
        k = int(k)
        conjunto = set()
        for i in range(len(self.estados)-1, -1,-1):
            if k % 2 == 1:
                conjunto.add(str(i))
                k -= 1
            k = k >> 1
        return conjunto
    
# ======= Determinizar =========

    def determinizar(self):
        # gerar epsilon fecho e remover epsilon do alfabeto
        self.gerarEpsilonFecho()
        if '&' in self.alfabeto:
            self.alfabeto.remove('&')

        # gerar as novas transicoes
        novasTransicoes = {}
        visitados = set()
        epsilonEstadoInicial = self.epsilonFechos[self.estadoInicial]
        filaEstados = [epsilonEstadoInicial]
        # enquanto tiver estados a serem visitados
        while len(filaEstados) > 0:
            estadosAtuais = filaEstados.pop()
            visitados.add(self.traduzir(estadosAtuais))
            # crio um conjunto de estados que vao ser alcancados pelo 
            # conjunto de estados atuais para cada caracter do alfabeto
            for c in self.alfabeto:
                estadosTransicao = set()
                for e in estadosAtuais:
                    if e in self.transicoes and c in self.transicoes[e]:
                        for p in self.transicoes[e][c]:
                            estadosTransicao.update(self.epsilonFechos[p])
                # conjunto de estados recebe uma codificacao 'binaria' para cada estado presente
                # e adiciono uma transicao partindo da codigo do conj. atual de estados
                # por um char 'c' para um codigo do conj. alcancavel de estados
                if len(estadosTransicao) > 0:
                    if self.traduzir(estadosAtuais) not in novasTransicoes:
                        novasTransicoes[self.traduzir(estadosAtuais)] = {}
                    novasTransicoes[self.traduzir(estadosAtuais)][c] = self.traduzir(estadosTransicao)
                    if self.traduzir(estadosTransicao) not in visitados:
                        filaEstados.append(estadosTransicao)

        # gerar o AFD
        estadoInicial = self.traduzir(epsilonEstadoInicial)
        estados = set()
        estadosFinais = set()
        # estados alcancaveis
        for e in novasTransicoes:
            estados.add(e)
            for c in novasTransicoes[e]:
                estados.add(novasTransicoes[e][c])
        # estados estadosFinais
        for ce in estados:
            conjEstados = self.destraduzir(ce)
            for e in conjEstados:
                if e in self.estadosFinais:
                    estadosFinais.add(ce)
        # crio o afd
        afd = AFD(estados, self.alfabeto, estadoInicial, estadosFinais)
        # adiciono as transicoes
        for e in novasTransicoes:
            for c in novasTransicoes[e]:
                afd.addTransicao(e, c, novasTransicoes[e][c])
        # retorno o afd
        return afd
