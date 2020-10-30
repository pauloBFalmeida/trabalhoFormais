
class DefReg:

    def __init__(self, id, s):
        self.id = id

        # self.expressao = s

        self.cadeias = []

        self.expressoes = []

        inicio = 0
        i = 0
        while i < len(s):
            c = s[i]
            if c in ['(', ' ', ')', '*', '?', '+', '|', '[', ']']:
                if s[inicio:i] != '' and s[inicio:i] not in self.cadeias:
                    self.cadeias.append(s[inicio:i])
                inicio = i+1
            i += 1

        # print(self.expressoes)

    def pedirRefs(self):
        return self.cadeias

    def receberRefs(self, resolucoes):
        for e in self.cadeias:
            if e in resolucoes:
                
