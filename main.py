import numpy as np
import math

matriz = None
si = None
matrizFixa = [
    [0,5,7,6,8],
    [5,0,3,4,6],
    [7,3,0,2,5],
    [6,4,2,0,3],
    [8,6,5,3,0]
]

def solucaoInicialFixa():
    return np.array([0,1,2,3,4])

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

def sucessor(solucao, n, matriz):
    suc = solucao.copy()
    n1 = np.random.randint(0,n)
    while True:
        n2 = np.random.randint(0,n)
        if n2 != n1:
            break
    aux = suc[n1]
    suc[n1] = suc[n2]
    suc[n2] =  aux
    vs = avaliar(n, suc, matriz)
    return suc, vs

def tempera(si, vi, matriz, ti, tf, fr):
    sa = si.copy()
    va = vi

    sb = sa.copy() 
    vb = va

    t = ti
    n = len(sa)
    while t > tf:
        
        sn, vn = sucessor(sa, n, matriz)
        if vn < va :
            sa =  sn
            va = vn
        else:
            d = vn - va
            ale = np.random.uniform(0,1)
            aux = math.exp(-d/t)
            if ale < aux:
                sa = sn
                va = vn
        if va < vb :
            vb = va
            sb = sa.copy()
        t *= fr
    return sb, vb


def preparar_problema(tipo, n=None):
    
    if tipo == "FIXO":
        matriz = np.array(matrizFixa)
        n = len(matriz)
        si = np.array([0,1,2,3,4])  # solução fixa

    elif tipo == "ALEATORIO":
        if n is None:
            raise ValueError("Informe o tamanho para problema aleatório")
        matriz = gerarProblema(n)
        si = gerarSolucao(n)

    else:
        raise ValueError("Tipo inválido")

    return matriz, si, n

def executar_metodo(metodo, matriz, si, n, tmax=None, ti=None, tf=None, fr=None):

    vi = avaliar(n, si, matriz)

    if metodo == "SE":
        return subida_da_encosta(matriz, n, si)

    elif metodo == "SET":
        if tmax is None:
            raise ValueError("TMAX não informado")
        return subida_da_encosta_tentativas(matriz, n, tmax)

    elif metodo == "TE":
        if None in (ti, tf, fr):
            raise ValueError("Parâmetros da têmpera não informados")
        return tempera(si, vi, matriz, ti, tf, fr)
    else:
        raise ValueError(f"Método inválido: {metodo}")


def analise_tabela(matriz, si, n):

    resultados = []

    vi = avaliar(n, si, matriz)

    # ───── SE ─────
    sol, val = subida_da_encosta(matriz, n, si)
    resultados.append(("SE", "-", vi - val))

    # ───── SET ─────
    configs_set = [
        ("TMAX=N", n),
        ("TMAX=2N", 2*n),
        ("TMAX=N/2", int(n/2))
    ]

    for nome, tmax in configs_set:
        sol, val = subida_da_encosta_tentativas(matriz, n, tmax)
        resultados.append(("SET", nome, vi - val))

    # ───── TÊMPERA ─────
    configs_te = [
        ("TI=100 TF=0.1 FR=0.8", 100, 0.1, 0.8),
        ("TI=200 TF=0.1 FR=0.8", 200, 0.1, 0.8),
        ("TI=500 TF=0.1 FR=0.8", 500, 0.1, 0.8),
        ("TI=200 TF=0.1 FR=0.9", 200, 0.1, 0.9),
        ("TI=500 TF=0.1 FR=0.9", 500, 0.1, 0.9),
        ("TI=200 TF=0.01 FR=0.9", 200, 0.01, 0.9),
        ("TI=500 TF=0.01 FR=0.9", 500, 0.01, 0.9),
    ]

    for nome, ti, tf, fr in configs_te:
        sol, val = tempera(si, vi, matriz, ti, tf, fr)
        resultados.append(("TE", nome, vi - val))

    return resultados