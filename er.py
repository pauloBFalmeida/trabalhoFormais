from defreg import *
from nodo import Nodo

class ER():

# ======= Criacao =========

    def __init__(self, definicoes):
        self.instancias = {}
        # self.defs = []

        print("def")
        for d in definicoes:
            if len(d) > 0:
                print(d)
                l = d.split(":")
                newDef = DefReg(l[0], l[1][1:])
                self.instancias[l[0]] = newDef
        print("donedefs")

        itlist = [id for id in self.instancias]

        for i in range(0,10):
            self.instancias[str(i)] = DefReg(str(i), str(i), unicoCaractere=True)
            self.instancias[str(i)].forcarExpressoes()

        for i in 'abcdefghijklmnopqrstuvwxyz':
            self.instancias[i] = DefReg(i, i, unicoCaractere=True)
            self.instancias[i].forcarExpressoes()

        for i in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            self.instancias[i] = DefReg(i, i, unicoCaractere=True)
            self.instancias[i].forcarExpressoes()

        for id in itlist:
            refs = self.instancias[id].pedirRefs()
            resolucoes = []
            nchar = [] # número de referências em cada resolução
            print('refs')
            modoExp = False
            expPropria = ""
            for ref in refs:
                ref = ref.strip()
                print(ref)
                if ref == ']':
                    modoExp = False
                    print("criando nova!")
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
                        print(f'cadeia == {self.instancias[exp].cadeias}')
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
            # print("doneRefs")

            self.instancias[id].receberRefs(resolucoes, nchar)


    def converterParaAFD(self): pass
