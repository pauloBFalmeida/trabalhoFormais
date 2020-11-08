# -*- coding: utf-8 -*-
# Universidade Federal de Santa Catarina
# Departamento de Informática e Estatística
# Alunos: Paulo Barbato Fogaça de Almeida, Wesly Carmesini Ataide
# Data: 07/11/2020


# ======= AF ===========

class ErroNoAutomato(Exception):
    pass

class EstadoInexistente(ErroNoAutomato):
    def __init__(self, estado):
        self.message = "O estado " + estado + " não existe."
        super().__init__(self.message)

class SimboloInexistente(ErroNoAutomato):
    def __init__(self, simbolo):
        self.message = "O símbolo " + simbolo + " não existe."
        super().__init__(self.message)

class TransicaoInexistente(ErroNoAutomato):
    def __init__(self, estadoInicial, simbolo):
        self.message = f"A transição delta({estadoInicial},{simbolo}) é vazia."
        super().__init__(self.message)

# ======= GR ===========

class ErroNaGramatica(Exception):
    def __init__(self, estado):
        self.message = "Ocorreu um erro na gramatica."
        super().__init__(self.message)

class GramaticaNaoRegular(ErroNaGramatica):
    def __init__(self, estado):
        self.message = "Gramatica nao e regular."
        super().__init__(self.message)
