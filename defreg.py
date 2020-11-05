from nodo import Nodo

class DefReg:

    def __init__(self, id, s):
        self.id = id

        # self.expressao = s

        self.cadeias = []

        self.expressoes = []
        self.operacoes = []

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

    def criarArvore(self):
        operacoes = self.expressoes




        #while there are tokens to be read:
        #read a token.
        #if the token is a number, then:
        #push it to the output queue.
        #else if the token is a function then:
        #push it onto the operator stack 
        #else if the token is an operator then:
        #while ((there is an operator at the top of the operator stack)
        #        and ((the operator at the top of the operator stack has greater precedence)
        #            or (the operator at the top of the operator stack has equal precedence and the token is left associative))
        #        and (the operator at the top of the operator stack is not a left parenthesis)):
        #    pop operators from the operator stack onto the output queue.
        #push it onto the operator stack.
        #else if the token is a left parenthesis (i.e. "("), then:
        #push it onto the operator stack.
        #else if the token is a right parenthesis (i.e. ")"), then:
        #while the operator at the top of the operator stack is not a left parenthesis:
        #    pop the operator from the operator stack onto the output queue.
        #/* If the stack runs out without finding a left parenthesis, then there are mismatched parentheses. */
        #if there is a left parenthesis at the top of the operator stack, then:
        #    pop the operator from the operator stack and discard it
        #/* After while loop, if operator stack not null, pop everything to output queue */
        #if there are no more tokens to read then:
        #while there are still operator tokens on the stack:
        #/* If the operator token on the top of the stack is a parenthesis, then there are mismatched parentheses. */
        #pop the operator from the operator stack onto the output queue.

        print(operacoes)
        for i in operacoes:
            if isinstance(i, DefReg):
                i.criarArvore()
            if i in ['*', '?', '+', '|']:
                pass



