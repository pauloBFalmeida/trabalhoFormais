from defreg import *
from nodo import Nodo

class ER():
    def __init__(self, definicoes):
        self.instancias = {}
        # self.defs = []

        for d in definicoes:
            if len(d) != 0:
                l = d.split(":")
                newDef = DefReg(l[0], l[1][1:])
                self.instancias[l[0]] = newDef

        itlist = [id for id in self.instancias]
        for id in itlist:
            refs = self.instancias[id].pedirRefs()
            resolucoes = []
            for ref in refs:
                if ref in self.instancias:
                    resolucoes.append(self.instancias[ref])
                    # aqui a gente cuidaria dos [0-9]/[a-z]
                elif ref in ['(', ' ', ')', '*', '?', '+', '|', '[', ']']:
                    resolucoes.append(ref)
                else:
                    nova = DefReg(ref, ref)
                    nova.forcarExpressoes()
                    self.instancias[ref] = nova
                    resolucoes.append(nova)

            self.instancias[id].receberRefs(resolucoes)

        for i in self.instancias:
            print(i)
            print(self.instancias[i])

        print()
        for i in self.instancias:
            print(self.instancias[i].cadeias)
            print(self.instancias[i].expressoes)


    def converterParaAFD(self):
        n = Nodo(1)



                

