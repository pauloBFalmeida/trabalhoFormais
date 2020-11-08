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
    er = ER(linhas)
    return er

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
        elif "nomes" in comando:
            nomesObjetos()
        elif "print" in comando:
            menuPrintar(args)
        elif "import" in comando:
            menuImportar(args)
        elif "export" in comando:
            menuExportar(args)
        elif "editar" in comando:
            menuEditar(args)
        elif "metodos" in comando:
            menuMetodos(args)
        elif "sair" in comando:
            rodando = False
            
# ========== Menu Help =========

def menuHelp():
    print("/help         - para exibir novamente os comandos")
    print("/nomes        - para exibir os nomes dos objetos criados")
    print("/print        - para exibir o objeto no terminal")
    print("/import       - para exibir o menu de importacao de arquivos")
    print("/export       - para exibir o menu de exportacao de arquivos")
    print("/editar       - para exibir o menu de edicao de objetos")
    print("/metodos      - para exibir o menu de metodos de objetos")
    print("/sair         - para terminar o programa (objetos nao exportados serao perdidos)")
    
# ========== Nome dos Objetos =========

def nomesObjetos():
    if len(objetos) < 1:
        print("nenhum objeto criado ainda")
        return
    print("lista de objetos criados:")
    for nome in objetos:
        tipo = str(objetos[nome].__class__.__name__)
        print("- "+nome + " <"+ tipo +">")
        
# ========== Menu Printrar =========

def menuPrintar(*args):
    # input nome
    args = args[0]
    if args:
        nome = args[0]
        args = []
    else:
        print("<nome do objeto>")
        nome = input()
    if nome not in objetos:
        print("nao existe um objeto com esse nome")
        return
    # printar
    objetos[nome].printar()
    
# ========== Menu Importar =========

def menuImportar(*args):
    # input
    args = args[0]
    if args:
        entrada = args
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

# ========== Menu Exportar =========

def menuExportar(*args):
    # input
    args = args[0]
    if args:
        entrada = args
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
    
# ========== Menu Editar =========

def menuEditar(*args):
    args = args[0]
    if args:
        entrada = args
        args = []
    else:
        print("<nome objeto>")
        print("nome objeto: nome do objeto")
        entrada = input().split(' ')

    nome = entrada[0]
    if nome not in objetos:
        print("nao existe um objeto com esse nome")
        return

    obj = objetos[nome]

    if isinstance(obj, AFD) or isinstance(obj, AFND):
        print("editando " + nome + "...")
        modoEdicaoAF(obj)
    elif isinstance(obj, GR):
        print("editando " + nome + "...")
        modoEdicaoGR(obj)
    elif isinstance(obj, ER):
        print("editando " + nome + "...")
        modoEdicaoER(obj)

def modoEdicaoAF(obj):

    def helpEdicao():
        print("\ncomandos possíveis")
        print("    #/add estados <estado>")
        print("    #/add alfabeto <simbolo>")
        print("    #/add transicao <estado antes> <simbolo> <estado depois>")
        print("    #/remove estados <estado>")
        print("    #/remove alfabeto <simbolo>")
        print("    #/remove transicao <estado antes> <simbolo> <estado depois>")
        print("    #/sair")
        print("    #/computar <entrada>")
        print("    #/print")

    helpEdicao()
    while True:
        entrada = input('#/').split(' ')
        if len(entrada) == 0:
            continue
        if entrada[0] == "sair":
            break
        if entrada[0] == "computar":
            ret = obj.computar(entrada[1])
            print(entrada[1]+(" nao" if not ret else "")+" pertence a linguagem")
            continue
        if entrada[0] == "print":
            obj.printar()
            continue
        if len(entrada) < 3:
            print("comando nao reconhecido")
            helpEdicao()
        else:
            op, edit, args = entrada[0], entrada[1], entrada[2:]
            if op == "add" and edit == "estados":
                estado = args[0]
                obj.addEstado(estado)
            elif op == "add" and edit == "alfabeto":
                simbolo = args[0]
                obj.addAlfabeto(simbolo)
            elif op == "add" and edit == "transicao":
                if len(args) == 3:
                    obj.addTransicao(args[0], args[1], args[2])
                else:
                    print("comando nao reconhecido")
                    helpEdicao()
            elif op == "remove" and edit == "estados":
                estado = args[0]
                obj.remEstado(estado)
            elif op == "remove" and edit == "alfabeto":
                simbolo = args[0]
                obj.remAlfabeto(simbolo)
            elif op == "remove" and edit == "transicao":
                if len(args) == 3:
                    obj.remTransicao(args[0], args[1], args[2])
                else:
                    print("comando nao reconhecido")
                    helpEdicao()
            else:
                print("comando nao reconhecido")
                helpEdicao()

def modoEdicaoGR(obj):
    def helpEdicao():
        print("\ncomandos possíveis")
        print("    #/add naoterminal  <nao terminal>")
        print("    #/add terminal <terminal>")
        print("    #/add producao <lado esquerdo> <lado direito>")
        print("    #/remove naoterminal <nao terminal>")
        print("    #/remove terminal <terminal>")
        print("    #/remove producao <lado esquerdo> <lado direito>")
        print("    #/sair")
        print("    #/derivar <profundidade>")
        print("    #/print")

    helpEdicao()
    while True:
        entrada = input('#/').split(' ')
        if len(entrada) == 0:
            continue
        if entrada[0] == "sair":
            break
        if entrada[0] == "derivar":
            obj.derivar(int(entrada[1]))
            continue
        if entrada[0] == "print":
            obj.printar()
            continue
        if len(entrada) < 3:
            print("comando nao reconhecido")
            helpEdicao()
        else:
            op, edit, args = entrada[0], entrada[1], entrada[2:]

            if op == "add" and edit == "naoterminal":
                naoterminal = args[0]
                obj.addNaoTerminal(naoterminal)
            elif op == "add" and edit == "terminal":
                terminal = args[0]
                obj.addTerminal(terminal)
            elif op == "add" and edit == "producao":
                if len(args) == 2:
                    obj.addProducao(args[0], args[1])
                else:
                    print("comando nao reconhecido")
                    helpEdicao()
            elif op == "remove" and edit == "naoterminal":
                naoterminal = args[0]
                obj.remNaoTerminal(naoterminal)
            elif op == "remove" and edit == "terminal":
                terminal = args[0]
                obj.remTerminal(terminal)
            elif op == "remove" and edit == "producao":
                if len(args) == 2:
                    obj.remProducao(args[0], args[1])
                else:
                    print("comando nao reconhecido")
                    helpEdicao()
            else:
                print("comando nao reconhecido")
                helpEdicao()
                
def modoEdicaoER(obj):
    def helpEdicao():
        print("\ncomandos possíveis")
        print("    #/add <nome da definicao> <expressao>")
        print("    #/remove <nome da definicao>")
        print("    #/sair")
        print("    #/print")

    helpEdicao()
    while True:
        entrada = input('#/').split(' ')
        if len(entrada) == 0:
            continue
        if entrada[0] == "sair":
            novas_definicoes = obj.getDefinicoes()
            obj = ER(novas_definicoes)
            break
        if entrada[0] == "print":
            obj.printar()
            continue
        if len(entrada) < 2:
            print("comando nao reconhecido")
            helpEdicao()
        else:
            op, args = entrada[0], entrada[1:]

            if op == "add":
                if len(entrada) == 3:
                    definicao, expressao = args[0], args[1]
                    obj.addDefinicao(definicao, expressao)
                else:
                    print("comando nao reconhecido")
                    helpEdicao()
            elif op == "remove":
                definicao = args[0]
                obj.remDefinicao(definicao)
            else:
                print("comando nao reconhecido")
                helpEdicao()

# ========== Menu Metodos =========

def menuMetodos(*args):
    args = args[0]
    # input nome
    if args:
        nome = args[0]
        args = []
    else:
        print("<nome do objeto>")
        nome = input()
    if nome not in objetos:
        print("nao existe um objeto com esse nome")
        return
    obj = objetos[nome]
    # ======== AFND ==========
    if isinstance(obj, AFND):
        print("metodos para AFND")
        print("    #/ajustar(NomeEstados)")
        print("    #/computar")
        print("    #/determinizar")
        print("    #/print")
        print("    #/sair")
        while True:
            print()
            comando = input("#/")
            if "sair" in comando:
                break
            elif "ajustar" in comando:
                obj.ajustarNomeEstados()
                print(nome+" teve ajuste no nome dos estados")
            elif "computar" in comando:
                print("entrada a ser computada:")
                entrada = input()
                ret = obj.computar(entrada)
                print(entrada+" "+("nao " if not ret else "")+"pertence a linguagem")
            elif "determinizar" in comando:
                print("nome do novo AFD:")
                nome2 = input()
                if nome2 in objetos:
                    print("ja existe um objeto com esse nome")
                    continue
                objetos[nome2] = obj.determinizar()
                print("novo AFD criado com o nome "+nome2)
            elif "print" in comando:
                obj.printar()
    # ======== AFD ==========
    elif isinstance(obj, AFD):
        print("metodos para AFD")
        print("    #/ajustar(NomeEstados)")
        print("    #/minimizar")
        print("    #/converter(ParaGR)")
        print("    #/computar")
        print("    #/interseccao")
        print("    #/uniao")
        print("    #/print")
        print("    #/sair")
        while True:
            print()
            comando = input("#/")
            if "sair" in comando:
                break
            elif "ajustar" in comando:
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
                    continue
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
                    continue
                print("nome para o novo AFD da "+comando+":")
                nome3 = input()
                if nome3 in objetos:
                    print("ja existe um objeto com esse nome")
                    continue
                obj2 = objetos[nome2]
                if ("uniao" in comando):
                    objetos[nome3] = obj.uniao(obj2)
                else:
                    objetos[nome3] = obj.interseccao(obj2)
                print(nome3+" contem a "+comando+" entre "+nome+" e "+nome2)
            elif "print" in comando:
                obj.printar()
    # ======== GR ==========
    elif isinstance(obj, GR):
        print("metodos para GR")
        print("    #/ajustar(NomeProducoes)")
        print("    #/derivar")
        print("    #/converter(ParaAFND)")
        print("    #/print")
        print("    #/sair")
        while True:
            print()
            comando = input("#/")
            if "sair" in comando:
                break
            elif "ajustar" in comando:
                obj.ajustarNomeProducoes()
                print(nome+" teve ajuste no nome das producoes")
            elif "derivar" in comando:
                print("profundidade: (tamanho de simbolos da cadeia de saida)")
                prof = int(input())
                obj.derivar(prof)
            elif "converter" in comando:
                print("nome do novo AFND:")
                nome2 = input()
                if nome2 in objetos:
                    print("ja existe um objeto com esse nome")
                    continue
                objetos[nome2] = obj.converterParaAFND()
                print("novo AFND criado com o nome "+nome2)
            elif "print" in comando:
                obj.printar()
    # ======== ER ==========
    elif isinstance(obj, ER):
        print("metodos para ER")
        print("    #/converter(ParaAFD) <nome da er (opcional)>")
        print("    #/print")
        print("    #/sair")
        while True:
            print()
            entrada = input("#/").split(" ")
            comando = entrada[0]
            if "sair" in comando:
                break
            if "converter" in comando:
                print("nome do novo AFD:")
                nome2 = input()
                if nome2 in objetos:
                    print("ja existe um objeto com esse nome")
                    continue
                if len(entrada) > 1:
                    afd = obj.converterParaAFD(entrada[1])
                else:
                    afd = obj.converterParaAFD(None)
                objetos[nome2] = afd
                print("novo AFD criado com o nome "+nome2)
            elif "print" in comando:
                obj.printar()

# ========= Execucao ===========
if __name__ == "__main__":
    main()
