class Nodo():
    def __init__(self, item):
        self.item = item
        self.filhoEsq = None
        self.filhoDir = None
        self.nullable = None
        self.firstPos = set()
        self.lastPos  = set()

    def getFirstPos(self):
        if len(self.firstPos) > 0:
            return self.firstPos