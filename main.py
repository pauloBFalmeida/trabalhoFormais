def lerArquivoAF(arquivo):
    with open(arquivo, "r") as file:
        linhas = file.read().split('\n')
        nEstados = linhas[0]
        estadoInicial = linhas[1]
        estadosFinais = linhas[2].split(',')
        transicoes = []
        for linha in linhas[4:]:
            transicoes.append(linha.split(','))

arquivo = input('nome do arquivo:\n')
lerArquivoAF(arquivo)