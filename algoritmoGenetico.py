import numpy as np
import math
import random

matriz = None
si = None
matrizFixa = [
    [0,5,7,6,8],
    [5,0,3,4,6],
    [7,3,0,2,5],
    [6,4,2,0,3],
    [8,6,5,3,0]
]

def popInicial(n,tp):
    populacao = []
    for i in range(n):
        populacao.append(np.random.permutation(tp))

    return populacao



def avaliar(n, solucao, matriz):
    distancia = 0
    for i in range(n - 1):
        distancia += matriz[solucao[i]][solucao[i + 1]]
    distancia += matriz[solucao[n - 1]][solucao[0]]
    return distancia

def fitness(solucao, matriz):
    return 1 / (avaliar(len(solucao), solucao, matriz) + 1)

def normalizarFitness(fit):
    total = sum(fit)
    return [f / total for f in fit]

def ordenar(populacao, fitness):
    pares = list(zip(fitness, populacao))
    pares.sort(key=lambda x: x[0], reverse=True)
    fitness_ord = [p[0] for p in pares]
    pop_ord     = [p[1] for p in pares]
    return pop_ord, fitness_ord

def selecao(populacao, fitness, metodo):
    tp = len(populacao)
    if metodo == 'roleta':
        return Roleta(fitness, tp)
    elif metodo == 'torneio':
        return Torneio(tp, fitness)
    else:
        raise ValueError(f"Método '{metodo}' inválido. Use 'roleta' ou 'torneio'.")


def Roleta(fitness, tp):
    ale = random.uniform(0, 1)
    ind = 0
    soma = fitness[ind]
    while soma < ale and ind < tp - 1:
        ind += 1
        soma += fitness[ind]
    return ind

def Torneio(tp, fitness):
    p1 = random.randrange(tp)
    p2 = random.randrange(tp)
    if fitness[p1] > fitness[p2]:
        return p1
    else:
        return p2
    
# ---------------------------------------------------------------------
# Cruzamento (baseado no AG do professor, adaptado ao formato vetor)
def cruzamento(p1, p2, ponto, n):
    d1 = np.concatenate((p1[0:ponto], p2[ponto:n]))
    d2 = np.concatenate((p2[0:ponto], p1[ponto:n]))
    return d1, d2

# ---------------------------------------------------------------------
# Mutação por troca (translocação) - igual ao professor
def mutacao2(d, n):
    pos1 = random.randrange(n)
    pos2 = random.randrange(n)
    d[pos1], d[pos2] = d[pos2], d[pos1]
    return d

def ajustaRestricao(desc, qd, corte, n):

    for i in range(qd):

        filho = list(desc[i])

        # primeira parte é preservada
        primeira_parte = set(filho[:corte])

        usados_segunda = set()
        repetidos = []

        # percorre apenas a segunda parte
        for j in range(corte, n):

            gene = filho[j]

            if gene in primeira_parte:
                repetidos.append(j)

            elif gene in usados_segunda:
                repetidos.append(j)

            else:
                usados_segunda.add(gene)

        # genes válidos presentes no filho
        usados = primeira_parte.union(usados_segunda)

        # genes que faltam para completar a permutação
        faltantes = []

        for gene in range(n):
            if gene not in usados:
                faltantes.append(gene)

        random.shuffle(faltantes)

        # substitui somente as posições inválidas
        for pos in repetidos:
            filho[pos] = faltantes.pop()

        desc[i] = np.array(filho)

    return desc

# ---------------------------------------------------------------------
# Ajusta restrição: garante que cada filho seja uma permutação válida
# (versão que preenche a parte após o corte com os genes faltantes,
#  sorteados aleatoriamente, sem repetição)
def ajustaRestricaoSimples(desc, qd, corte, n):
    for i in range(qd):
        visto = set()
        faltantes = [x for x in range(n) if x not in desc[i][:corte]]
        random.shuffle(faltantes)
        novo = list(desc[i][:corte])
        for j in range(corte, n):
            gene = desc[i][j]
            if gene in visto or gene in novo:
                gene = faltantes.pop(0)
            visto.add(gene)
            novo.append(gene)
        desc[i] = np.array(novo)
    return desc

# ---------------------------------------------------------------------
# Gera descendentes via seleção, cruzamento e mutação
def gerarDescendentes(pop, fit, tp, n, tc, tm, metodo_selecao):
    qd = 2 * tp
    desc = np.zeros((qd, n), int)

    # ponto de corte aleatório, sorteado uma vez por geração (igual ao professor)
    corte = random.randint(1, n - 1)

    i = 0

    while i < qd:

        idx1 = selecao(pop, fit, metodo_selecao)
        idx2 = selecao(pop, fit, metodo_selecao)

        p1 = pop[idx1]
        p2 = pop[idx2]

        if random.uniform(0, 1) <= tc:
            d1, d2 = cruzamento(p1, p2, corte, n)
        else:
            d1 = p1.copy()
            d2 = p2.copy()

        if random.uniform(0, 1) <= tm:
            d1 = mutacao2(d1, n)

        if random.uniform(0, 1) <= tm:
            d2 = mutacao2(d2, n)

        desc[i] = d1
        desc[i + 1] = d2

        i += 2

    return desc, qd, corte

# ---------------------------------------------------------------------
# Nova população: elitismo + substituição pelos descendentes
def novaPopulacao(pop, desc, tp, ig):
    elite = int(ig * tp)
    nova = []
    for i in range(elite):
        nova.append(pop[i])
    for i in range(tp - elite):
        nova.append(desc[i])
    return nova

# ---------------------------------------------------------------------
# Algoritmo Genético principal
def algoritmoGenetico(matriz, tp, n, ng, tc, tm, ig, metodo_selecao='torneio'):
    pop = popInicial(tp, n)

    fit = [fitness(ind, matriz) for ind in pop]
    fit = normalizarFitness(fit)
    pop, fit = ordenar(pop, fit)

    melhor_inicial = pop[0]

    for g in range(ng):
        desc, qd, corte = gerarDescendentes(pop, fit, tp, n, tc, tm, metodo_selecao)
        desc = ajustaRestricao(desc, qd, corte, n)

        fit_desc = [fitness(ind, matriz) for ind in desc]
        fit_desc = normalizarFitness(fit_desc)
        desc, fit_desc = ordenar(desc, fit_desc)

        pop = novaPopulacao(pop, desc, tp, ig)

        fit = [fitness(ind, matriz) for ind in pop]
        fit = normalizarFitness(fit)
        pop, fit = ordenar(pop, fit)

    melhor_final = pop[0]

    return melhor_inicial, melhor_final, \
           avaliar(n, melhor_inicial, matriz), \
           avaliar(n, melhor_final, matriz)

def gerarProblema(n):
    matriz = np.random.randint(low=10, high=100, size=(n, n))
    np.fill_diagonal(matriz, 0)
    return matriz

def individuoValido(ind, n):
    return len(ind) == n and len(set(ind)) == n and all(0 <= x < n for x in ind)

def testeCompleto():
    N = 50

    TP = 100
    NG = 200

    TC = 0.9
    TM = 0.15

    IG = 0.10

    print("=" * 80)
    print("GERANDO MATRIZ DE TESTE")
    print("=" * 80)

    matriz = gerarProblema(N)

    np.set_printoptions(
        linewidth=500,
        threshold=np.inf
    )

    print(matriz)

    print("\n" + "=" * 80)
    print("TESTE DA POPULAÇÃO INICIAL")
    print("=" * 80)

    pop = popInicial(TP, N)

    for i, ind in enumerate(pop):
        print(f"{i:02d} -> {list(ind)}")

    print("\nTodas as soluções possuem tamanho correto?")

    valido = all(len(ind) == N for ind in pop)

    print(valido)

    print("\n" + "=" * 80)
    print("TESTE DE FITNESS")
    print("=" * 80)

    fit = [fitness(ind, matriz) for ind in pop]

    for i, f in enumerate(fit):
        print(f"Indivíduo {i}: {f:.8f}")

    fit = normalizarFitness(fit)

    print("\nSoma fitness normalizado:")
    print(sum(fit))

    print("\n" + "=" * 80)
    print("TESTE DE SELEÇÃO")
    print("=" * 80)

    idx1 = selecao(pop, fit, "torneio")
    idx2 = selecao(pop, fit, "roleta")

    print("Torneio selecionou:", idx1)
    print("Roleta selecionou :", idx2)

    print("\n" + "=" * 80)
    print("TESTE DE CRUZAMENTO")
    print("=" * 80)

    corte = random.randint(1, N - 1)

    d1, d2 = cruzamento(
        pop[idx1],
        pop[idx2],
        corte,
        N
    )

    print("Pai 1:")
    print(list(pop[idx1]))

    print("\nPai 2:")
    print(list(pop[idx2]))

    print("\nFilho 1:")
    print(list(d1))

    print("\nFilho 2:")
    print(list(d2))

    print("\n" + "=" * 80)
    print("TESTE DE MUTAÇÃO")
    print("=" * 80)

    d1 = mutacao2(d1, N)
    d2 = mutacao2(d2, N)

    print("Filho 1 mutado:")
    print(list(d1))

    print("\nFilho 2 mutado:")
    print(list(d2))

    print("\n" + "=" * 80)
    print("TESTE DE AJUSTE DE RESTRIÇÃO")
    print("=" * 80)

    desc = np.array([d1, d2])

    print("\nANTES DO AJUSTE")

    for i in range(2):
        print(f"\nFilho {i}")
        print(list(desc[i]))
        print("Genes únicos:", len(set(desc[i])))

    desc = ajustaRestricao(
        desc,
        2,
        corte,
        N
    )

    print("\nDEPOIS DO AJUSTE")

    for i in range(2):

        print(f"\nDescendente {i}")

        print(list(desc[i]))

        genes_unicos = len(set(desc[i]))

        print("Genes únicos:", genes_unicos)

        if genes_unicos == N:
            print("PERMUTAÇÃO VÁLIDA")
        else:

            print("ERRO NA RESTRIÇÃO")

            faltando = [
                x for x in range(N)
                if x not in desc[i]
            ]

            vistos = set()
            repetidos = []

            for gene in desc[i]:
                if gene in vistos:
                    repetidos.append(gene)
                else:
                    vistos.add(gene)

            print("Corte:", corte)
            print("Repetidos:", repetidos)
            print("Faltando:", faltando)

            raise Exception("AJUSTE DE RESTRIÇÃO FALHOU")

    print("\n" + "=" * 80)
    print("TESTE DE GERAÇÃO DE DESCENDENTES")
    print("=" * 80)

    desc, qd, corte = gerarDescendentes(
        pop,
        fit,
        TP,
        N,
        TC,
        TM,
        "torneio"
    )

    desc = ajustaRestricao(
        desc,
        qd,
        corte,
        N
    )

    erro = False

    for i in range(qd):

        if len(set(desc[i])) != N:

            print("\nERRO ENCONTRADO")
            print("Filho:", i)
            print("Corte:", corte)
            print(list(desc[i]))
            print("Genes únicos:", len(set(desc[i])))

            erro = True
            break

    if not erro:
        print("Todos os descendentes são válidos.")

    print("\n" + "=" * 80)
    print("EXECUTANDO ALGORITMO GENÉTICO")
    print("=" * 80)

    melhor_inicial, melhor_final, custo_inicial, custo_final = algoritmoGenetico(
        matriz,
        TP,
        N,
        NG,
        TC,
        TM,
        IG,
        "torneio"
    )

    print("\nMelhor Inicial")
    print(list(melhor_inicial))
    print("Custo:", custo_inicial)

    print("\nMelhor Final")
    print(list(melhor_final))
    print("Custo:", custo_final)

    print("\nMelhoria obtida:")
    print(custo_inicial - custo_final)

    print("\n" + "=" * 80)
    print("VALIDAÇÃO FINAL")
    print("=" * 80)

    print("Genes únicos:", len(set(melhor_final)))

    if len(set(melhor_final)) == N:
        print("Melhor solução é uma permutação válida.")
    else:
        print("ERRO: solução inválida.")
        print(list(melhor_final))

def testeQualidadeAG():

    N = 50
    TP = 100
    NG = 200

    TC = 0.9
    TM = 0.15
    IG = 0.10

    print("=" * 80)
    print("TESTE DE QUALIDADE DO ALGORITMO GENÉTICO")
    print("=" * 80)

    matriz = gerarProblema(N)

    resultados = []
    melhorias = []

    for rodada in range(30):

        melhor_inicial, melhor_final, custo_inicial, custo_final = algoritmoGenetico(
            matriz,
            TP,
            N,
            NG,
            TC,
            TM,
            IG,
            "torneio"
        )

        melhoria = (
            (custo_inicial - custo_final)
            / custo_inicial
        ) * 100

        resultados.append(custo_final)
        melhorias.append(melhoria)

        print(
            f"Execução {rodada+1:02d} | "
            f"Inicial={custo_inicial:.0f} | "
            f"Final={custo_final:.0f} | "
            f"Melhoria={melhoria:.2f}%"
        )

    print("\n" + "=" * 80)
    print("ESTATÍSTICAS")
    print("=" * 80)

    print(f"Melhor custo encontrado : {min(resultados):.0f}")
    print(f"Pior custo encontrado   : {max(resultados):.0f}")
    print(f"Custo médio             : {sum(resultados)/len(resultados):.2f}")

    print()

    print(f"Maior melhoria          : {max(melhorias):.2f}%")
    print(f"Menor melhoria          : {min(melhorias):.2f}%")
    print(f"Melhoria média          : {sum(melhorias)/len(melhorias):.2f}%")

    print("\n" + "=" * 80)
    print("COMPARAÇÃO COM SOLUÇÕES ALEATÓRIAS")
    print("=" * 80)

    custos_aleatorios = []

    for _ in range(100):

        individuo = np.random.permutation(N)

        custo = avaliar(
            N,
            individuo,
            matriz
        )

        custos_aleatorios.append(custo)

    media_aleatoria = sum(custos_aleatorios) / len(custos_aleatorios)

    print(f"Custo médio aleatório : {media_aleatoria:.2f}")
    print(f"Custo médio do AG     : {sum(resultados)/len(resultados):.2f}")

    ganho = (
        (media_aleatoria - (sum(resultados)/len(resultados)))
        / media_aleatoria
    ) * 100

    print(f"Ganho sobre aleatório : {ganho:.2f}%")


if __name__ == "__main__":
    testeQualidadeAG()