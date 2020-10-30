
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
                if s[inicio:i] != '':
                    self.cadeias.append(s[inicio:i])
                self.cadeias.append(c)
                inicio = i+1
            i += 1

        # print(self.cadeias)

    def pedirRefs(self):
        return self.cadeias

    def receberRefs(self, resolucoes):
        for i in range(len(self.cadeias)):
            if self.cadeias[i] in ['(', ' ', ')', '*', '?', '+', '|', '[', ']']:
                self.expressoes.append(self.cadeias[i])
                continue
            self.expressoes.append(resolucoes[i])

    def forcarExpressoes(self):
        self.expressoes = self.cadeias
