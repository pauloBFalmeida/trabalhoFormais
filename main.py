from afd import *
from afnd import *
from gr import *
from er import *
from defreg import *

# ========= AF ===========
def criarAFD(nEstados, alfabeto, estadoInicial, estadosFinais, transicoes):
    afd = AFD([str(i) for i in range(int(nEstados))], alfabeto, estadoInicial, estadosFinais)
    for t in transicoes:
        afd.addTransicao(t[0],t[1],t[2])
    return afd

def criarAFND(nEstados, alfabeto, estadoInicial, estadosFinais, transicoes):
    afnd = AFND([str(i) for i in range(int(nEstados))], alfabeto, estadoInicial, estadosFinais)
    for t in transicoes:
        for estadosFinais in t[2].split('-'):
            afnd.addTransicao(t[0],t[1],estadosFinais)
    return afnd

def lerArquivoAF(arquivo, isAFD):
    with open(arquivo, "r") as file:
        linhas = file.read().split('\n')

    nEstados = linhas[0]
    estadoInicial = linhas[1]
    estadosFinais = linhas[2].split(',')
    alfabeto = linhas[3].split(',')
    transicoes = []
    for linha in linhas[4:]:
        if len(linha) == 0:
            break
        transicoes.append(linha.split(','))

    if isAFD:
        afd = criarAFD(nEstados, alfabeto, estadoInicial, estadosFinais, transicoes)
        return afd
    else:
        afnd = criarAFND(nEstados, alfabeto, estadoInicial, estadosFinais, transicoes)
        return afnd

# ========= GR ===========
def lerArquivoGR(arquivo):
    with open(arquivo, "r") as file:
        linhas = file.read().split('\n')

    gr = GR()
    for linha in linhas:
        if len(linha) <= 0:
            break
        linha = linha.split("->")
        simbolo = linha[0].strip()
        for c in linha[1]:
            if c.islower():
                gr.addTerminal(c)
            elif c.isupper():
                gr.addNaoTerminal(c)
        gr.addNaoTerminal(simbolo)
        derivacoes = list(map(lambda x: x.strip(), linha[1].split("|")))
        for derivacao in derivacoes:
            gr.addProducao(simbolo, derivacao)
    return gr

# ========= ER ===========
def lerArquivoER(arquivo):
    with open(arquivo, "r") as file:
        linhas = file.read().split('\n')

    julia = ER(linhas)
    for e in julia.instancias:
        # print(f"e = {e}" )
        # print(julia.instancias[e].expressoes)
        # julia.instancias[e].prepararExpressao()
        #julia.instancias[e].criarArvore()
        #julia.instancias[e].printarArvore()
        julia.instancias[e].converterParaAFD()
        julia.instancias[e].printarArvore()

# ========= Main ===========
objetos = {}

def main():
    menuHelp()
    rodando = True
    while rodando:
        print()
        entrada = input('/').split(' ')
        comando = entrada[0]
        args = entrada[1:]
        if "help" in comando:
            menuHelp()
        elif "nomesObjetos" in comando:
            nomesObjetos()
        elif "printar" in comando:
            menuPrintar(args)
        elif "importar" in comando:
            menuImportar(args)
        elif "exportar" in comando:
            menuExportar(args)
        elif "editar" in comando:
            menuEditar(args)
        elif "metodos" in comando:
            menuMetodos(args)
        elif "sair" in comando:
            rodando = False

def menuHelp():
    print("/help         - para exibir novamente os comandos")
    print("/nomesObjetos - para exibir os nomes dos objetos criados")
    print("/printar      - para exibir o objeto no terminal")
    print("/importar     - para exibir o menu de importacao de arquivos")
    print("/exportar     - para exibir o menu de exportacao de arquivos")
    print("/editar       - para exibir o menu de edicao de objetos")
    print("/metodos      - para exibir o menu de metodos de objetos")
    print("/sair         - para terminar o programa (objetos nao exportados serao perdidos)")

def nomesObjetos():
    if len(objetos) < 1:
        print("nenhum objeto criado ainda")
        return
    print("lista de objetos criados:")
    for nome in objetos:
        tipo = str(objetos[nome].__class__.__name__)
        print("- "+nome + " <"+ tipo +">")

def menuPrintar(*args):
    # input nome
    if args:
        nome = args[0][0]
        args = []
    else:
        print("<nome do objeto>")
        nome = input()
    if nome not in objetos:
        print("nao existe um objeto com esse nome")
        return
    # printar
    objetos[nome].printar()

def menuImportar(*args):
    # input
    if args:
        entrada = args[0]
        args = []
    else:
        print("<nome desejado> <tipo> <nome do arquivo>")
        print("nome desejado: nome para o objeto a ser criado")
        print("tipos: afd afnd gr er")
        print("nome do arquivo: nome do arquivo com extensao")
        entrada = input().split(' ')
    # nome
    nome = entrada[0]
    if nome in objetos:
        print("ja existe um objeto com esse nome")
        return
    # arquivo
    arquivo = entrada[2]
    # tipo
    tipo = entrada[1]
    if "afd" in tipo:
        objetos[nome] = lerArquivoAF(arquivo, True)
    elif "afnd" in tipo:
        objetos[nome] = lerArquivoAF(arquivo, False)
    elif "gr" in tipo:
        objetos[nome] = lerArquivoGR(arquivo)
    elif "er" in tipo:
        objetos[nome] = lerArquivoER(arquivo)
    else:
        print("tipo nao encontrado")
        return
    print(tipo+" foi criado com o nome: "+nome)

def menuExportar(*args):
    # input
    if args:
        entrada = args[0]
        args = []
    else:
        print("<nome objeto> <nome do arquivo>")
        print("nome objeto: nome do objeto")
        print("nome do arquivo: nome do arquivo com extensao")
        entrada = input().split(' ')
    # nome
    nome = entrada[0]
    if nome not in objetos:
        print("nao existe um objeto com esse nome")
        return
    # arquivo
    arquivo = entrada[1]
    # exportar
    objetos[nome].exportarParaArquivo(arquivo)
    print("objeto "+nome+" foi exportado com o nome: "+arquivo)

def menuEditar():
    #addEstado
    #addAlfabeto
    #addTransicao
    #remEstado
    #remAlfabeto
    #remTransicao
    pass

def menuMetodos(*args):
    # input nome
    if args:
        nome = args[0][0]
        args = []
    else:
        print("<nome do objeto>")
        nome = input()
    if nome not in objetos:
        print("nao existe um objeto com esse nome")
        return
    obj = objetos[nome]
    # AFND
    if isinstance(obj, AFND):
        print("metodos para AFND")
        print("computar determinizar")
        comando = input()
        if "computar" in comando:
            print("entrada a ser computada:")
            entrada = input()
            ret = obj.computar(entrada)
            print(entrada+" "+("nao " if not ret else "")+"pertence a linguagem")
        elif "determinizar" in comando:
            print("nome do novo AFD:")
            nome2 = input()
            if nome2 in objetos:
                print("ja existe um objeto com esse nome")
                return
            objetos[nome2] = obj.determinizar()
            print("novo AFD criado com o nome "+nome2)
    # AFD
    elif isinstance(obj, AFD):
        print("metodos para AFD")
        print("ajustar(NomeEstados) minimizar converter(ParaGR) computar interseccao uniao")
        comando = input()
        if "ajustar" in comando:
            obj.ajustarNomeEstados()
            print(nome+" teve ajuste no nome dos estados")
        elif "minimizar" in comando:
            obj.minimizar()
            print(nome+" foi minimizado")
        elif "converter" in comando:
            print("nome da nova GR:")
            nome2 = input()
            if nome2 in objetos:
                print("ja existe um objeto com esse nome")
                return
            objetos[nome2] = obj.converterParaGR()
            print("nova gr criada com o nome "+nome2)
        elif "computar" in comando:
            print("entrada a ser computada:")
            entrada = input()
            ret = obj.computar(entrada)
            print(entrada+" "+("nao " if not ret else "")+"pertence a linguagem")
        elif ("interseccao" in comando) or ("uniao" in comando):
            print("nome do outro AFD para fazer a "+comando+":")
            nome2 = input()
            if nome2 not in objetos:
                print("nao existe um objeto com esse nome")
                return
            print("nome para o novo AFD da "+comando+":")
            nome3 = input()
            if nome3 in objetos:
                print("ja existe um objeto com esse nome")
                return
            obj2 = objetos[nome2]
            if ("uniao" in comando):
                objetos[nome3] = obj.uniao(obj2)
            else:
                objetos[nome3] = obj.interseccao(obj2)
            print(nome3+" contem a "+comando+" entre "+nome+" e "+nome2)
    # GR
    elif isinstance(obj, GR):
        print("metodos para GR")
        print("ajustar(NomeProducoes) derivar converter(ParaAFND)")
        comando = input()
        if "ajustar" in comando:
            obj.ajustarNomeProducoes()
        elif "derivar" in comando:
            print("profundidade: (tamanho de simbolos da cadeia de saida)")
            prof = int(input())
            obj.derivar(prof)
        elif "converter" in comando:
            print("nome do novo AFND:")
            nome2 = input()
            if nome2 in objetos:
                print("ja existe um objeto com esse nome")
                return
            objetos[nome2] = obj.converterParaAFND()
            print("novo AFND criado com o nome "+nome2)
    elif isinstance(obj, ER):
        print("metodos para ER")


# ========= Execucao ===========
if __name__ == "__main__":
    main()