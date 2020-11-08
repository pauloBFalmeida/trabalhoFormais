from defreg import *
from nodo import Nodo

class ER():

# ======= Criacao =========

    def __init__(self, definicoes):
        self.instancias = {}
        self.definicoes = {}
        self.lastErId = None
        
        # [0-9]
        for i in range(0,10):
            self.instancias[str(i)] = DefReg(str(i), str(i), unicoCaractere=True)
            self.instancias[str(i)].forcarExpressoes()
        # [a-z]
        for i in [chr(i) for i in range(ord('a'), ord('z')+1)]:
            self.instancias[i] = DefReg(i, i, unicoCaractere=True)
            self.instancias[i].forcarExpressoes()
        # [A-Z]
        for i in [chr(i) for i in range(ord('A'), ord('Z')+1)]:
            self.instancias[i] = DefReg(i, i, unicoCaractere=True)
            self.instancias[i].forcarExpressoes()

        # criar definicoes
        itlist = []
        for d in definicoes:
            if len(d) > 0:
                l = d.split(":")
                newDef = DefReg(l[0], l[1][1:])
                self.instancias[l[0]] = newDef
                self.definicoes[l[0]] = l[1][1:]
                itlist.append(l[0])
        self.lastErId = itlist[-1]

        for id in itlist:
            refs = self.instancias[id].pedirRefs()
            resolucoes = []
            nchar = [] # número de referências em cada resolução
            modoExp = False
            expPropria = ""
            for ref in refs:
                ref = ref.strip()
                if ref == ']':
                    modoExp = False
                    # considerando os casos digito-digito, letra-letra
                    exps = [expPropria[i*3:(i+1)*3] for i in range(len(expPropria)//3)]
                    for exp in exps:
                        resolverCaracteres = []
                        inicio, fim = exp.split('-')
                        r = inicio
                        resolverCaracteres.append(self.instancias[inicio])
                        # [inicio, fim]
                        while inicio != fim:
                            inicio = chr(ord(inicio)+1)
                            resolverCaracteres.append("|")
                            resolverCaracteres.append(self.instancias[inicio])
                            r += ("|"+inicio)
                        self.instancias[exp] = DefReg(exp, r, expressaoPropria=True)
                        self.instancias[exp].receberRefs(resolverCaracteres, [1 for i in range(len(resolverCaracteres))])
                        resolucoes.append(self.instancias[exp])
                        nchar.append(1)
                    continue
                if modoExp:
                    expPropria += ref
                    continue
                if ref == '[':
                    modoExp = True
                    continue

                if ref in self.instancias:
                    resolucoes.append(self.instancias[ref])
                    nchar.append(1)
                elif ref in ['(', ' ', ')', '*', '?', '+', '|', '[', ']']:
                    resolucoes.append(ref)
                    nchar.append(1)
                else:
                    # uma cadeia de caracteres simplesmente...
                    for c in ref.strip():
                        if c not in self.instancias:
                            nova = DefReg(c, c, True)
                            nova.forcarExpressoes()
                            self.instancias[c] = nova
                            resolucoes.append(nova)
                        else:
                            resolucoes.append(self.instancias[c])
                    nchar.append(len(ref.strip()))

            self.instancias[id].receberRefs(resolucoes, nchar)

# ======== Editar ===========

    def addDefinicao(self, id, er):
        self.definicoes[id] = er

    def remDefinicao(self, id):
        if id in self.definicoes:
            del self.definicoes[id]

    def getDefinicoes(self):
        r = []
        for id in self.definicoes:
            r.append(f'{id}: {self.definicoes[id]}')
        return r
    
# ======== Converter para AFD ===========

    def converterParaAFD(self, er):
        if not er:
            er = self.lastErId
        afd = self.instancias[er].converterParaAFD()
        return afd

# ======== Print ===========
    def printar(self):
        for id in self.definicoes:
            print(f'{id}: {self.definicoes[id]}')
