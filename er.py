
class ER():
    def __init__(self, definicoes):
        self.instancias = {}
        # self.defs = []

        for d in definicoes:
            l = d.split(":")
            newDef = DefReg(l[0], l[1][1:])
            self.instancias[l[0]] = newDef

        for id in self.instancias:
            refs = self.instancias[id].pedirRefs()
            resolucoes = []
            for ref in refs:
                if ref in self.instancias:
                    resolucoes.append((ref, self.instancias[ref]))
                    # aqui a gente cuidaria dos [0-9]/[a-z]
