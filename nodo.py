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
            self.nullable = filhoEsq.calcularNullable() or filhoDir.calcularNullable()
        elif self.item == ".":
            self.nullable = filhoEsq.calcularNullable() and filhoDir.calcularNullable()
        elif self.item  == "*":
            self.nullable = True
        elif self.item == "?":
            self.nullable = True
        elif self.item == "+":
            self.nullable = filhoEsq.calcularNullable()
        return self.nullable

    def calcularPos(self, pos, dict_posicoes):
        if self.filhoEsq is None and self.filhoDir is None:
            self.pos = pos[0]
            dict_posicoes[pos[0]] = self
            pos[0]+=1
        else:
            self.filhoEsq.calcularPos(pos)
            if self.filhoDir is not None:
                self.filhoDir.calcularPos(pos)
        return

    def calcularFirstPos(self):
        if self.filhoEsq is None and self.filhoDir is None:
            if self.item == "&":
                self.firstPos = set()
            else:
                self.firstPos = {self.pos}
        elif self.item == "|":
            self.firstPos = filhoEsq.calcularFirstPos().union(filhoDir.calcularFirstPos())
        elif self.item == ".":
            if filhoEsq.nullable:
                self.firstPos = filhoEsq.calcularFirstPos().union(filhoDir.calcularFirstPos())
            else:
                self.firstPos = filhoEsq.calcularFirstPos()
        elif self.item  == "*":
            self.firstPos = filhoEsq.calcularFirstPos()
        elif self.item == "?":
            self.firstPos = filhoEsq.calcularFirstPos()
        elif self.item == "+":
            self.firstPos = filhoEsq.calcularFirstPos()
        return self.firstPos


    def calcularLastPos(self):
        if self.filhoEsq is None and self.filhoDir is None:
            if self.item == "&":
                self.lastPos = set()
            else:
                self.lastPos = {self.pos}
        elif self.item == "|":
            self.lastPos = filhoEsq.calcularLastPos().union(filhoDir.calcularLastPos())
        elif self.item == ".":
            if filhoDir.nullable:
                self.lastPos = filhoEsq.calcularLastPos().union(filhoDir.calcularLastPos())
            else:
                self.lastPos = filhoDir.calcularLastPos()
        elif self.item  == "*":
            self.lastPos = filhoEsq.calcularLastPos()
        elif self.item == "?":
            self.lastPos = filhoEsq.calcularLastPos()
        elif self.item == "+":
            self.lastPos = filhoEsq.calcularLastPos()
        return self.lastPos

    def calcularFollowPos(self, follow_pos):
        if self.filhoEsq is None and self.filhoDir is None:
            return

        if self.item == ".":
            for i in self.filhoEsq.lastPos:
                follow_pos[i] = follow_pos[i].union(self.filhoDir.firstPos)
        elif self.item  == "*":
            for i in self.lastPos:
                follow_pos[i] = follow_pos[i].union(self.firstPos)
        elif self.item == "+":
            for i in self.lastPos:
                follow_pos[i] = follow_pos[i].union(self.firstPos)

        self.filhoEsq.calcularFollowPos(follow_pos)
        if self.filhoDir is not None:
            self.filhoDir.calcularFollowPos(follow_pos)

    def getFirstPos(self):
        if len(self.firstPos) > 0:
            return self.firstPos
