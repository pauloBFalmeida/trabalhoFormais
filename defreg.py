from nodo import Nodo

class DefReg:

    def __init__(self, id, s, unicoCaractere=False, expressaoPropria=False):
        self.id = id
        self.unicoCaractere = unicoCaractere
        self.expressaoPropria = expressaoPropria
        # self.expressao = s

        self.cadeias = []

        self.expressoes = []
        self.operacoes = []
        self.raiz = None

        inicio = 0
        i = 0
        while i < len(s):
            c = s[i]
            if c == " ":
                i += 1
                continue
            if c in ['(', ' ', ')', '*', '?', '+', '|', '[', ']']:
                if s[inicio:i] != '':
                    self.cadeias.append(s[inicio:i])
                self.cadeias.append(c)
                inicio = i+1
            i += 1
        if s[-1] not in ['(', ' ', ')', '*', '?', '+', '|', '[', ']']:
            if s[inicio:i] != '':
                self.cadeias.append(s[inicio:i])

        # print(self.cadeias)

    def pedirRefs(self):
        return self.cadeias

    def receberRefs(self, resolucoes, nchar):
        i = 0
        r = 0
        while i < len(self.cadeias) and r < len(resolucoes):
            for k in range(nchar[i]):
                self.expressoes.append(resolucoes[r+k])
            r += nchar[i]
            i += 1


    def forcarExpressoes(self):
        # print("para id=" + self.id)
        # print("forcando expressao = " + str(self.cadeias))
        self.expressoes = self.cadeias

    def prec(self, op):
        if op == "*" or op == "?" or op == "+":
            return 2
        elif op == "|" or op == ".":
            return 1
        else:
            return -1

    def prepararExpressao(self):
        # explicitar concatenações
        nova_expressao = [self.expressoes[0]]
        for i in range(len(self.expressoes) - 1):
            if (self.expressoes[i] not in ['(', '*', '?', '+', '|', '[', ']'] and \
                self.expressoes[i+1] not in [ ')', '*', '?', '+', '|', '[', ']']) or \
                (self.expressoes[i] in [')', '*', '?', '+', ']'] and \
                 (self.expressoes[i+1] in ['(', '['] or isinstance(self.expressoes[i+1], DefReg))):

                nova_expressao.append(".")
            nova_expressao.append(self.expressoes[i+1])

        self.expressoes = nova_expressao
        print(self.expressoes)

        # transformar para prefixa
        expressoes = self.expressoes
        expressoes.reverse()
        output = []
        stack = []
        for i in expressoes:
            if isinstance(i, DefReg):
                output.append(i)
            elif i == '*' or i == "?" or i == "+":
                stack.append(i)
            elif i == "|" or i == ".":
                while len(stack) > 0 and self.prec(stack[-1]) >= self.prec(i):
                    output.append(stack.pop())
                stack.append(i)
            elif i == ')':
                stack.append(i)
            elif i == '(':
                while stack[-1] != ')':
                    output.append(stack.pop())
                stack.pop() # parênteses
            else:
                output.append(i)
        while len(stack) > 0:
            output.append(stack.pop())
        output.reverse()
        print("OUTPUT!")
        print(output)
        self.operacoes = output

    def criarArvore(self):
        # retorna a raiz
        if self.unicoCaractere:
            self.raiz = Nodo(self.cadeias[0])
            return self.raiz

        self.prepararExpressao()
        operacoes = self.operacoes
        c = operacoes[0]
        index = [1]

        raiz = Nodo(c)
        filhoEsq, filhoDir = None, None
        if isinstance(c, DefReg):
            self.raiz = c.criarArvore()
            return self.raiz
        elif c == '*' or c == '?' or c == '+':
            filhoEsq = self.avaliarNodo(1, index)
        elif c == '|' or c == '.':
            # operador binário
            filhoEsq, filhoDir = self.avaliarNodo(2, index)

        raiz.filhoEsq = filhoEsq
        raiz.filhoDir = filhoDir

        self.raiz = raiz
        return raiz

    def printarArvore(self):
        self.printarNodo(self.raiz)

    def printarNodo(self, nodo):

        if nodo.filhoEsq is None:
            fe = "/"
        else:
            fe = nodo.filhoEsq.item

        if nodo.filhoDir is None:
            fd = "/"
        else:
            fd = nodo.filhoDir.item

        print(f'{nodo.item} -> {fe}, -> {fd}')


        if nodo.filhoEsq is not None:
            self.printarNodo(nodo.filhoEsq)

        if nodo.filhoDir is not None:
            self.printarNodo(nodo.filhoDir)


    def avaliarNodo(self, noperandos, index):
        # index é uma lista para acessarmos de qualquer nodo da árvore de recursão

        c = self.operacoes[index[0]]
        filhoEsq, filhoDir = None, None
        if isinstance(c, DefReg):
            index[0] += 1
            filhoEsq = c.criarArvore()
        elif c == '*' or c == '?' or c == '+':
            # operador unário
            index[0] += 1
            filhoEsq = self.avaliarNodo(1, index)
        elif c == '|' or c == '.':
            # operador binário
            index[0] += 1
            filhoEsq, filhoDir = self.avaliarNodo(2, index)

        nodoEsq = Nodo(c)
        if isinstance(c, DefReg):
            nodoEsq = filhoEsq # retorna a raiz da arvore dessa definição
        else:
            nodoEsq.filhoEsq = filhoEsq
            nodoEsq.filhoDir = filhoDir


        if noperandos == 1:
            return nodoEsq

        d = self.operacoes[index[0]]
        filhoEsq, filhoDir = None, None
        if isinstance(d, DefReg):
            index[0] += 1
            filhoEsq = d.criarArvore()
        elif d == '*' or d == '?' or d == '+':
            # operador unário
            index[0] += 1
            filhoEsq = self.avaliarNodo(1, index)
        elif d == '|' or d == '.':
            # operador binário
            index[0] += 1
            filhoEsq, filhoDir = self.avaliarNodo(2, index)

        nodoDir = Nodo(d)
        if isinstance(d, DefReg):
            nodoDir = filhoEsq # retorna a raiz da arvore dessa definição
        else:
            nodoDir.filhoEsq = filhoEsq
            nodoDir.filhoDir = filhoDir
        return nodoEsq, nodoDir

    def calcularNullable(self):
        self.raiz.calcularNullable()

    def calcularPos(self):
        dict_posicoes = {}
        self.raiz.calcularPos([1], dict_posicoes)
        return dict_posicoes

    def calcularFirstPos(self):
        self.raiz.calcularFirstPos()

    def calcularFollowPos(self, follow_pos):
        self.raiz.calcularFollowPos(follow_pos)

    def converterParaAFD(self):
        tag = DefReg('#', '#')
        tag.forcarExpressoes
        backup = self.expressoes

        self.expressoes = ['('] + self.expressoes + [')', tag]
        self.criarArvore()
        self.calcularNullable()

        dict_posicoes = self.calcularPos()

        self.calcularFirstPos()
        self.calcularLastPos()
        follow_pos = {}
        for i in dict_posicoes:
            follow_pos[i] = set()
        self.calcularFollowPos(follow_pos)

        self.expressoes = backup
