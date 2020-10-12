class ErroNoAutomato(Exception):
    pass

class EstadoInexistente(ErroNoAutomato):
    def __init__(self, estado):
        self.message = "O estado " + estado + " não existe."
        super().__init__(self.message)

class SimboloInexistente():
    def __init__(self, simbolo):
        self.message = "O símbolo " + simbolo + " não existe."
        super().__init__(self.message)

class TransicaoInexistente():
    def __init__(self, estadoInicial, simbolo):
        self.message = f"A transição delta({estadoInicial},{simbolo}) é vazia."
        super().__init__(self.message)