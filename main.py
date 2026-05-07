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
    return np.array([0, 2, 4, 1, 3])

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

def sucessores(n, atual, matriz, pos):
    melhor = atual
    vm = avaliar(n, atual, matriz)

    for i in range(n):
        if i != pos:
            suc = atual.copy()
            suc[i], suc[pos] = suc[pos], suc[i]

            vs = avaliar(n, suc, matriz)

            if vs < vm:
                melhor = suc
                vm = vs

    return melhor, vm

def subida_da_encosta(matriz, n, solucao_inicial):

    solucao_atual = solucao_inicial.copy()
    valor_atual = avaliar(n, solucao_atual, matriz)

    melhorou = True

    while melhorou:
        melhorou = False
        melhor_vizinho = solucao_atual.copy()
        melhor_valor = valor_atual

        pos = np.random.randint(0, n)

        melhor_vizinho, melhor_valor = sucessores(n, solucao_atual, matriz, pos)

        if melhor_valor < valor_atual:
            solucao_atual = melhor_vizinho
            valor_atual = melhor_valor
            melhorou = True

    return solucao_atual, valor_atual

def subida_da_encosta_tentativas(matriz, n, tentativas,solucao_inicial):

    solucao_atual = solucao_inicial.copy()
    valor_atual = avaliar(n, solucao_atual, matriz)

    t = 0
    posicoes = list(np.random.permutation(n))
    while t<tentativas:
        if not posicoes:
            posicoes = list(np.random.permutation(n))
        
        pos = posicoes.pop()
        solucao_nova, valor_nova = sucessores(n,solucao_atual,matriz,pos)

        if valor_nova<valor_atual:
            solucao_atual = solucao_nova.copy()
            valor_atual = valor_nova
            posicoes = list(np.random.permutation(n))
            t = 0
        else:
            t = t + 1
        
    return solucao_atual, valor_atual

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
            if va < vb:
                vb = va
                sb = sa.copy()
        else:
            d = vn - va
            ale = np.random.uniform(0,1)
            aux = math.exp(-d/t)
            if ale < aux:
                sa = sn.copy()
                va = vn
        t *= fr
    return sb, vb


def preparar_problema(tipo, n=None):
    
    if tipo == "FIXO":
        matriz = np.array(matrizFixa)
        n = len(matriz)
        si = solucaoInicialFixa()

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
        return subida_da_encosta_tentativas(matriz, n, tmax, si)

    elif metodo == "TE":
        if None in (ti, tf, fr):
            raise ValueError("Parâmetros da têmpera não informados")
        return tempera(si, vi, matriz, ti, tf, fr)
    else:
        raise ValueError(f"Método inválido: {metodo}")


def analise_tabela(matriz, si, n):

    resultados = []
    vi = avaliar(n, si, matriz)

    EXECUCOES = 30

    melhor_valor = float("inf")

    for _ in range(EXECUCOES):
        sol, val = subida_da_encosta(matriz, n, si)
        if val < melhor_valor:
            melhor_valor = val

    ganho = vi - melhor_valor
    porcentagem = (ganho / vi) * 100
    resultados.append(("SE", "---", f"{porcentagem:.2f}%"))

    configs_set = [
        ("TMAX=N", n),
        ("TMAX=N/2", int(n/2)),
        ("TMAX=N/4", int(n/4))
    ]

    for nome, tmax in configs_set:
        melhor_valor = float("inf")

        for _ in range(EXECUCOES):
            sol, val = subida_da_encosta_tentativas(matriz, n, tmax, si)
            if val < melhor_valor:
                melhor_valor = val

        ganho = vi - melhor_valor
        porcentagem = (ganho / vi) * 100
        resultados.append(("SET", nome, f"{porcentagem:.2f}%"))

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
        melhor_valor = float("inf")

        for _ in range(EXECUCOES):
            sol, val = tempera(si, vi, matriz, ti, tf, fr)
            if val < melhor_valor:
                melhor_valor = val

        ganho = vi - melhor_valor
        porcentagem = (ganho / vi) * 100
        
        resultados.append(("TE", nome, f"{porcentagem:.2f}%"))
    return resultados