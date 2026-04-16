import numpy as np

matriz = None
si = None


def gerarProblema(n):
    matriz = np.random.randint(low=10, high=100, size=(n, n))
    np.fill_diagonal(matriz, 0)
    return matriz


def gerarSolucao(n):
    return np.random.permutation(n)


def avaliar(n, solucao, matriz):
    distancia = 0
    for i in range(n - 1):
        distancia += matriz[solucao[i]][solucao[i + 1]]
    distancia += matriz[solucao[n - 1]][solucao[0]]
    return distancia


def print_array(arr):
    print("\n".join(map(str, arr)))


def subida_da_encosta(matriz, n, solucao_inicial):

    solucao_atual = solucao_inicial.copy()
    valor_atual = avaliar(n, solucao_atual, matriz)

    melhorou = True

    while melhorou:
        melhorou = False
        melhor_vizinho = solucao_atual.copy()
        melhor_valor = valor_atual

        for i in range(n):
            for j in range(i + 1, n):
                nova_solucao = solucao_atual.copy()
                nova_solucao[i], nova_solucao[j] = nova_solucao[j], nova_solucao[i]

                valor_novo = avaliar(n, nova_solucao, matriz)

                if valor_novo < melhor_valor:
                    melhor_valor = valor_novo
                    melhor_vizinho = nova_solucao
                    melhorou = True

        if melhorou:
            solucao_atual = melhor_vizinho
            valor_atual = melhor_valor

    return solucao_atual, valor_atual

def subida_da_encosta_tentativas(matriz, n, tentativas):

    melhor_solucao = None
    melhor_valor = float("inf")

    usadas = set()
    t = 0

    while t < tentativas:

        solucao_inicial = gerarSolucao(n)

        while tuple(solucao_inicial) in usadas:
            solucao_inicial = gerarSolucao(n)

        usadas.add(tuple(solucao_inicial))

        solucao_atual, valor_atual = subida_da_encosta(matriz, n, solucao_inicial)

        print(f"\nTentativa {t}:")
        print("Solução atual ->", solucao_atual)
        print("Valor atual->", valor_atual)
        print("Melhor valor ->", melhor_valor)

        if valor_atual < melhor_valor:
            melhor_valor = valor_atual
            melhor_solucao = solucao_atual

            t = 0
        else:
            t += 1

    return melhor_solucao, melhor_valor

n = int(input("Tamanho da Matrix: "))
tentativas = int(input("Número de tentativas: "))

matriz = gerarProblema(n)
si = gerarSolucao(n)

print("\nMatrix:")
print_array(matriz)
melhor_solucao, melhor_valor = subida_da_encosta_tentativas(matriz, n, tentativas)

print("Melhor solução: ", melhor_solucao)
print("Melhor valor: ", melhor_valor)


        