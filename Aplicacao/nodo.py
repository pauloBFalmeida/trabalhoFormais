# -*- coding: utf-8 -*-
# Universidade Federal de Santa Catarina
# Departamento de Informática e Estatística
# Alunos: Paulo Barbato Fogaça de Almeida, Wesly Carmesini Ataide
# Data: 07/11/2020

class Nodo():
    def __init__(self, item):
        self.item = item
        self.pos = -1
        self.filhoEsq = None
        self.filhoDir = None
        self.nullable = None
        self.firstPos = set()
        self.lastPos  = set()

# ========= Nullable ===========

    def calcularNullable(self):
        # nodo folha
        if self.filhoEsq is None and self.filhoDir is None:
            if self.item == "&":
                self.nullable = True
            else:
                self.nullable = False
        # nodo com filhos
        # | nullable se algum dos filhos forem
        elif self.item == "|":
            esq = self.filhoEsq.calcularNullable()
            dir = self.filhoDir.calcularNullable()
            self.nullable = esq or dir
        # . nullable se ambos os filhos forem
        elif self.item == ".":
            esq = self.filhoEsq.calcularNullable()
            dir = self.filhoDir.calcularNullable()
            self.nullable = esq and dir
        # * nullable sempre
        elif self.item  == "*":
            self.filhoEsq.calcularNullable()
            self.nullable = True
        # ? nullable sempre
        elif self.item == "?":
            self.filhoEsq.calcularNullable()
            self.nullable = True
        # + nullable se o filho unico for
        elif self.item == "+":
            self.nullable = self.filhoEsq.calcularNullable()
        return self.nullable
    
# ========= Pos ===========

    def calcularPos(self, pos, dict_posicoes):
        # nodo folha recebe a primeira posicao da lista de pos
        if self.filhoEsq is None and self.filhoDir is None:
            self.pos = pos[0]
            dict_posicoes[pos[0]] = self
            pos[0]+=1
        else:
            # calculo pos com base nos filhos
            self.filhoEsq.calcularPos(pos, dict_posicoes)
            if self.filhoDir is not None:
                self.filhoDir.calcularPos(pos, dict_posicoes)
        return
    
    def calcularFirstPos(self):
        # nodo folha
        if self.filhoEsq is None and self.filhoDir is None:
            if self.item == "&":
                self.firstPos = set()
            else:
                self.firstPos = {self.pos}
        # | uniao dos filhos
        elif self.item == "|":
            self.firstPos = self.filhoEsq.calcularFirstPos().union(self.filhoDir.calcularFirstPos())
        # . se filho a esq for nullable, uniao dos filhos, senao filho a esq
        elif self.item == ".":
            if self.filhoEsq.nullable:
                self.firstPos = self.filhoEsq.calcularFirstPos().union(self.filhoDir.calcularFirstPos())
            else:
                self.firstPos = self.filhoEsq.calcularFirstPos()
                self.filhoDir.calcularFirstPos()
        # * msm do filho unico
        elif self.item  == "*":
            self.firstPos = self.filhoEsq.calcularFirstPos()
        # ? msm do filho unico
        elif self.item == "?":
            self.firstPos = self.filhoEsq.calcularFirstPos()
        # + msm do filho unico
        elif self.item == "+":
            self.firstPos = self.filhoEsq.calcularFirstPos()
        return self.firstPos


    def calcularLastPos(self):
        # nodo folha
        if self.filhoEsq is None and self.filhoDir is None:
            if self.item == "&":
                self.lastPos = set()
            else:
                self.lastPos = {self.pos}
        # | uniao dos filhos
        elif self.item == "|":
            self.lastPos = self.filhoEsq.calcularLastPos().union(self.filhoDir.calcularLastPos())
        # . se filho dir for nullable, uniao dos filhos, senao filho a dir
        elif self.item == ".":
            if self.filhoDir.nullable:
                self.lastPos = self.filhoEsq.calcularLastPos().union(self.filhoDir.calcularLastPos())
            else:
                self.lastPos = self.filhoDir.calcularLastPos()
                self.filhoEsq.calcularLastPos()
        # * msm do filho unico
        elif self.item  == "*":
            self.lastPos = self.filhoEsq.calcularLastPos()
        # ? msm do filho unico
        elif self.item == "?":
            self.lastPos = self.filhoEsq.calcularLastPos()
        # + msm do filho unico
        elif self.item == "+":
            self.lastPos = self.filhoEsq.calcularLastPos()
        return self.lastPos
    
# ========= FollowPos ===========

    def calcularFollowPos(self, follow_pos):
        # nodo folha
        if self.filhoEsq is None and self.filhoDir is None:
            return

        # calcular followPos dos filhos
        self.filhoEsq.calcularFollowPos(follow_pos)
        if self.filhoDir is not None:
            self.filhoDir.calcularFollowPos(follow_pos)
            
        # calcular followPos
        if self.item == ".":
            for i in self.filhoEsq.lastPos:
                follow_pos[i] = follow_pos[i].union(self.filhoDir.firstPos)
        elif self.item  == "*":
            for i in self.lastPos:
                follow_pos[i] = follow_pos[i].union(self.firstPos)
        elif self.item == "+":
            for i in self.lastPos:
                follow_pos[i] = follow_pos[i].union(self.firstPos)
                
# ========= Getters ===========

    def getFirstPos(self):
        if len(self.firstPos) > 0:
            return self.firstPos
        
    def getLastPos(self):
        if len(self.lastPos) > 0:
            return self.lastPos