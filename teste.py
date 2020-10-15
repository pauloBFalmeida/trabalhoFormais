conjunto = list(map(int, input().split()))
estados = int(input())

def traduzir(conjunto, estados):
    k = 0
    for i in range(estados):
        if i in conjunto:
            k = (k << 1) + 1
        else:
            k = k << 1
    return k
print(traduzir(conjunto, estados))
