class Nodo():
    def __init__(self, item):
        self.item = item
        self.pos = -1
        self.filhoEsq = None
        self.filhoDir = None
        self.nullable = None
        self.firstPos = set()
        self.lastPos  = set()

    def calcularNullable(self):
        if self.filhoEsq is None and self.filhoDir is None:
            if self.item == "&":
                self.nullable = True
            else:
                self.nullable = False
        elif self.item == "|":
            esq = self.filhoEsq.calcularNullable()
            dir = self.filhoDir.calcularNullable()
            self.nullable = esq or dir
        elif self.item == ".":
            esq = self.filhoEsq.calcularNullable()
            dir = self.filhoDir.calcularNullable()
            self.nullable = esq and dir
        elif self.item  == "*":
            self.filhoEsq.calcularNullable()
            self.nullable = True
        elif self.item == "?":
            self.filhoEsq.calcularNullable()
            self.nullable = True
        elif self.item == "+":
            self.nullable = self.filhoEsq.calcularNullable()
        return self.nullable

    def calcularPos(self, pos, dict_posicoes):
        if self.filhoEsq is None and self.filhoDir is None:
            self.pos = pos[0]
            dict_posicoes[pos[0]] = self
            pos[0]+=1
        else:
            self.filhoEsq.calcularPos(pos, dict_posicoes)
            if self.filhoDir is not None:
                self.filhoDir.calcularPos(pos, dict_posicoes)
        return

    def calcularFirstPos(self):
        if self.filhoEsq is None and self.filhoDir is None:
            if self.item == "&":
                self.firstPos = set()
            else:
                self.firstPos = {self.pos}
        elif self.item == "|":
            self.firstPos = self.filhoEsq.calcularFirstPos().union(self.filhoDir.calcularFirstPos())
        elif self.item == ".":
            if self.filhoEsq.nullable:
                self.firstPos = self.filhoEsq.calcularFirstPos().union(self.filhoDir.calcularFirstPos())
            else:
                self.firstPos = self.filhoEsq.calcularFirstPos()
                self.filhoDir.calcularFirstPos()
        elif self.item  == "*":
            self.firstPos = self.filhoEsq.calcularFirstPos()
        elif self.item == "?":
            self.firstPos = self.filhoEsq.calcularFirstPos()
        elif self.item == "+":
            self.firstPos = self.filhoEsq.calcularFirstPos()
        return self.firstPos


    def calcularLastPos(self):
        if self.filhoEsq is None and self.filhoDir is None:
            if self.item == "&":
                self.lastPos = set()
            else:
                self.lastPos = {self.pos}
        elif self.item == "|":
            self.lastPos = self.filhoEsq.calcularLastPos().union(self.filhoDir.calcularLastPos())
        elif self.item == ".":
            if self.filhoDir.nullable:
                self.lastPos = self.filhoEsq.calcularLastPos().union(self.filhoDir.calcularLastPos())
            else:
                self.lastPos = self.filhoDir.calcularLastPos()
                self.filhoEsq.calcularLastPos()
        elif self.item  == "*":
            self.lastPos = self.filhoEsq.calcularLastPos()
        elif self.item == "?":
            self.lastPos = self.filhoEsq.calcularLastPos()
        elif self.item == "+":
            self.lastPos = self.filhoEsq.calcularLastPos()
        return self.lastPos

    def calcularFollowPos(self, follow_pos):
        if self.filhoEsq is None and self.filhoDir is None:
            return

        self.filhoEsq.calcularFollowPos(follow_pos)
        if self.filhoDir is not None:
            self.filhoDir.calcularFollowPos(follow_pos)

        if self.item == ".":
            for i in self.filhoEsq.lastPos:
                follow_pos[i] = follow_pos[i].union(self.filhoDir.firstPos)
        elif self.item  == "*":
            for i in self.lastPos:
                follow_pos[i] = follow_pos[i].union(self.firstPos)
        elif self.item == "+":
            for i in self.lastPos:
                follow_pos[i] = follow_pos[i].union(self.firstPos)


    def getFirstPos(self):
        if len(self.firstPos) > 0:
            return self.firstPos
        
    def getLastPos(self):
        if len(self.lastPos) > 0:
            return self.lastPos