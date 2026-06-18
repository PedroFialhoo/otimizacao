import numpy as np
import math
import pandas as pd
import itertools
import time
import random


matriz = None
si = None
matrizFixa = [
    [0, 58, 78, 91, 73, 18, 61, 63, 16, 99, 99, 53, 77, 68, 22, 60, 59, 54, 70, 42, 14, 57, 79, 59, 57, 52, 16, 55, 20, 26, 12, 98, 61, 83, 89, 48, 87, 46, 56, 92, 11, 20, 49, 33, 31, 53, 51, 31, 79, 43],
    [24, 0, 12, 91, 40, 49, 89, 58, 56, 73, 92, 19, 78, 98, 28, 96, 74, 34, 62, 53, 86, 20, 97, 27, 37, 67, 53, 62, 20, 90, 28, 61, 69, 23, 24, 80, 15, 42, 86, 45, 63, 75, 16, 56, 54, 81, 78, 67, 77, 65],
    [64, 32, 0, 78, 13, 51, 31, 68, 29, 13, 52, 84, 51, 74, 27, 41, 75, 83, 95, 36, 34, 12, 76, 54, 30, 23, 42, 21, 63, 13, 37, 61, 29, 97, 24, 81, 87, 45, 61, 69, 76, 85, 38, 63, 77, 36, 43, 13, 59, 14],
    [90, 48, 72, 0, 50, 42, 43, 24, 69, 42, 79, 19, 85, 49, 81, 66, 52, 27, 46, 59, 12, 75, 68, 90, 79, 55, 52, 26, 26, 23, 76, 96, 83, 50, 32, 43, 52, 77, 82, 56, 32, 31, 28, 95, 20, 32, 45, 45, 23, 63],
    [96, 24, 16, 17, 0, 27, 28, 37, 61, 45, 94, 20, 31, 28, 61, 54, 86, 99, 30, 83, 47, 18, 61, 93, 37, 64, 22, 31, 90, 88, 31, 62, 42, 24, 51, 69, 86, 35, 32, 45, 75, 67, 25, 61, 51, 27, 38, 53, 44, 14],
    [96, 13, 51, 23, 67, 0, 75, 50, 84, 75, 43, 96, 27, 16, 10, 98, 84, 66, 34, 99, 10, 74, 57, 31, 64, 60, 99, 34, 23, 33, 29, 17, 85, 93, 91, 53, 85, 58, 73, 80, 38, 27, 59, 37, 39, 57, 80, 75, 51, 14],
    [69, 34, 34, 99, 40, 36, 0, 66, 25, 25, 64, 32, 74, 47, 81, 67, 33, 38, 37, 78, 97, 41, 96, 29, 24, 10, 31, 79, 43, 67, 66, 90, 10, 36, 10, 47, 83, 18, 58, 96, 49, 83, 37, 74, 25, 81, 62, 80, 21, 60],
    [16, 64, 55, 49, 10, 18, 75, 0, 64, 41, 51, 84, 58, 81, 55, 84, 53, 67, 58, 59, 80, 43, 44, 51, 36, 62, 74, 46, 37, 56, 92, 67, 59, 25, 87, 71, 77, 93, 83, 11, 82, 55, 44, 69, 73, 39, 85, 66, 30, 36],
    [96, 95, 18, 55, 40, 71, 51, 86, 0, 10, 17, 50, 77, 22, 62, 39, 53, 48, 26, 85, 22, 50, 90, 78, 89, 70, 88, 39, 97, 21, 52, 76, 34, 31, 89, 48, 38, 60, 93, 59, 71, 47, 66, 36, 60, 88, 85, 87, 80, 53],
    [50, 74, 96, 93, 68, 89, 65, 60, 39, 0, 73, 46, 64, 49, 10, 28, 66, 30, 34, 76, 18, 15, 33, 54, 24, 98, 87, 99, 64, 97, 33, 49, 47, 43, 18, 54, 45, 78, 88, 47, 48, 47, 94, 15, 65, 72, 88, 45, 71, 60],
    [26, 60, 50, 75, 30, 37, 94, 14, 91, 28, 0, 23, 50, 76, 97, 13, 76, 84, 16, 66, 75, 14, 74, 51, 77, 22, 80, 14, 53, 69, 34, 83, 35, 58, 85, 85, 89, 83, 81, 72, 31, 87, 78, 53, 78, 48, 96, 49, 19, 34],
    [14, 68, 21, 45, 63, 63, 69, 67, 56, 58, 30, 0, 40, 32, 31, 50, 70, 77, 96, 64, 29, 12, 94, 77, 14, 77, 97, 88, 51, 83, 86, 25, 13, 74, 65, 11, 42, 59, 72, 52, 72, 14, 37, 81, 50, 11, 13, 57, 63, 85],
    [11, 15, 89, 40, 41, 70, 78, 63, 43, 60, 38, 28, 0, 33, 70, 22, 71, 97, 89, 43, 53, 23, 76, 26, 57, 59, 72, 81, 89, 93, 15, 11, 83, 58, 10, 70, 13, 81, 69, 58, 61, 99, 91, 11, 55, 85, 95, 47, 17, 86],
    [59, 77, 49, 90, 92, 41, 11, 36, 54, 63, 22, 24, 39, 0, 58, 15, 49, 10, 93, 36, 44, 94, 26, 14, 64, 67, 91, 11, 27, 92, 41, 37, 88, 25, 87, 69, 47, 23, 32, 96, 48, 44, 38, 74, 22, 81, 96, 50, 60, 84],
    [94, 37, 95, 20, 29, 47, 53, 96, 19, 39, 75, 25, 60, 69, 0, 90, 85, 13, 19, 78, 40, 55, 38, 23, 82, 53, 94, 43, 98, 20, 30, 46, 64, 73, 77, 26, 58, 70, 35, 17, 70, 83, 21, 43, 69, 81, 81, 62, 10, 53],
    [99, 41, 22, 96, 81, 25, 49, 97, 38, 48, 69, 80, 93, 83, 60, 0, 30, 50, 20, 76, 97, 34, 63, 98, 81, 87, 31, 56, 31, 66, 96, 92, 11, 61, 84, 44, 11, 36, 68, 24, 38, 16, 68, 36, 76, 52, 31, 61, 94, 48],
    [84, 98, 17, 81, 29, 55, 83, 71, 42, 94, 65, 71, 47, 78, 69, 24, 0, 53, 13, 16, 69, 88, 16, 87, 43, 99, 21, 94, 84, 39, 92, 42, 19, 31, 17, 26, 87, 43, 73, 68, 59, 80, 21, 29, 12, 88, 16, 87, 74, 98],
    [26, 47, 28, 84, 96, 24, 58, 85, 61, 68, 99, 11, 35, 14, 19, 81, 98, 0, 49, 46, 70, 16, 35, 49, 96, 29, 99, 58, 44, 26, 74, 62, 66, 61, 92, 73, 75, 67, 72, 66, 57, 81, 99, 46, 43, 78, 24, 50, 33, 16],
    [17, 15, 65, 68, 37, 58, 31, 32, 97, 65, 18, 47, 84, 24, 66, 84, 61, 57, 0, 34, 69, 66, 69, 89, 13, 22, 73, 57, 19, 53, 64, 72, 94, 96, 42, 45, 23, 29, 24, 11, 73, 34, 84, 53, 67, 32, 38, 50, 62, 18],
    [77, 62, 11, 21, 40, 39, 46, 81, 47, 72, 58, 39, 11, 32, 74, 72, 24, 52, 22, 0, 58, 40, 57, 17, 94, 89, 24, 74, 63, 53, 47, 95, 72, 51, 75, 58, 36, 71, 78, 49, 79, 27, 46, 59, 39, 99, 66, 57, 49, 43],
    [75, 10, 70, 85, 69, 86, 47, 57, 64, 97, 16, 45, 31, 64, 23, 64, 71, 72, 67, 85, 0, 66, 12, 73, 27, 91, 22, 92, 98, 89, 11, 53, 25, 98, 98, 63, 87, 50, 50, 34, 39, 52, 18, 28, 60, 93, 21, 10, 85, 53],
    [58, 59, 89, 34, 34, 88, 29, 32, 74, 18, 17, 39, 51, 49, 72, 67, 77, 96, 19, 23, 91, 0, 45, 57, 16, 54, 11, 95, 25, 75, 28, 10, 50, 50, 86, 46, 48, 26, 42, 73, 25, 21, 45, 71, 17, 16, 27, 60, 99, 66],
    [83, 14, 62, 83, 87, 23, 96, 50, 76, 32, 67, 88, 23, 33, 85, 47, 76, 72, 89, 23, 21, 25, 0, 65, 95, 37, 41, 38, 81, 55, 28, 72, 59, 95, 58, 50, 38, 65, 21, 30, 12, 12, 27, 75, 81, 34, 29, 55, 72, 90],
    [62, 17, 71, 93, 91, 49, 37, 27, 28, 68, 59, 79, 44, 63, 73, 81, 25, 74, 49, 92, 96, 16, 76, 0, 29, 70, 27, 99, 83, 15, 84, 77, 16, 42, 78, 72, 58, 29, 13, 27, 55, 54, 17, 13, 59, 13, 31, 19, 29, 81],
    [77, 39, 95, 77, 79, 40, 51, 76, 47, 45, 89, 81, 31, 48, 95, 95, 20, 22, 53, 22, 43, 87, 90, 77, 0, 15, 84, 19, 96, 88, 56, 71, 35, 88, 81, 34, 24, 11, 12, 59, 41, 49, 20, 70, 46, 13, 60, 92, 31, 23],
    [49, 24, 73, 39, 32, 12, 68, 70, 23, 58, 65, 85, 47, 23, 15, 81, 70, 50, 95, 52, 20, 27, 91, 90, 32, 0, 55, 45, 44, 30, 88, 92, 24, 90, 67, 30, 46, 60, 99, 92, 56, 23, 65, 49, 26, 69, 47, 66, 30, 85],
    [61, 79, 47, 96, 61, 85, 22, 54, 92, 92, 20, 51, 32, 58, 31, 70, 93, 19, 15, 77, 54, 72, 48, 24, 90, 83, 0, 61, 25, 52, 62, 90, 44, 77, 59, 14, 37, 59, 87, 78, 16, 50, 32, 35, 82, 49, 39, 70, 63, 56],
    [89, 79, 93, 66, 99, 41, 85, 81, 14, 11, 71, 36, 36, 56, 20, 34, 46, 35, 19, 66, 65, 80, 21, 87, 36, 77, 74, 0, 41, 98, 43, 47, 29, 67, 18, 40, 93, 21, 14, 43, 85, 76, 27, 16, 77, 73, 29, 67, 78, 58],
    [88, 69, 49, 33, 48, 66, 17, 62, 76, 52, 33, 17, 91, 56, 74, 55, 79, 89, 19, 32, 10, 14, 55, 35, 22, 49, 54, 99, 0, 36, 40, 72, 24, 81, 52, 66, 80, 50, 52, 64, 47, 42, 20, 99, 10, 98, 30, 40, 35, 26],
    [65, 42, 67, 33, 24, 72, 45, 14, 11, 70, 51, 78, 64, 94, 86, 19, 27, 75, 74, 15, 69, 27, 24, 67, 10, 43, 35, 85, 45, 0, 92, 62, 49, 76, 28, 43, 82, 72, 66, 64, 70, 28, 45, 21, 92, 56, 93, 55, 81, 53],
    [57, 82, 38, 51, 44, 72, 33, 25, 77, 36, 22, 92, 31, 10, 10, 91, 36, 27, 29, 15, 45, 23, 78, 63, 73, 31, 92, 17, 79, 49, 0, 15, 72, 91, 75, 91, 46, 37, 82, 34, 29, 91, 66, 19, 14, 78, 59, 41, 43, 39],
    [90, 74, 58, 80, 92, 91, 99, 71, 53, 91, 19, 31, 46, 22, 78, 92, 46, 32, 14, 34, 95, 73, 25, 99, 16, 27, 90, 16, 44, 83, 19, 0, 30, 88, 24, 87, 35, 67, 95, 10, 62, 80, 36, 88, 40, 25, 39, 84, 98, 76],
    [25, 72, 18, 46, 52, 17, 70, 36, 40, 96, 78, 21, 42, 69, 50, 15, 69, 49, 18, 56, 37, 36, 79, 35, 27, 25, 50, 12, 27, 40, 97, 73, 0, 49, 18, 81, 40, 15, 96, 21, 99, 21, 23, 59, 27, 42, 90, 63, 13, 78],
    [57, 43, 60, 95, 35, 55, 47, 48, 27, 54, 85, 51, 95, 69, 84, 26, 26, 29, 40, 97, 65, 89, 20, 80, 86, 63, 74, 69, 46, 80, 97, 80, 69, 0, 98, 24, 80, 90, 43, 47, 35, 77, 34, 32, 70, 16, 30, 40, 12, 81],
    [55, 99, 84, 56, 89, 90, 85, 15, 68, 41, 48, 32, 95, 72, 95, 54, 14, 30, 32, 99, 66, 96, 31, 37, 64, 50, 91, 76, 71, 96, 21, 20, 57, 28, 0, 65, 70, 91, 46, 38, 80, 97, 35, 53, 22, 33, 99, 67, 49, 43],
    [19, 60, 72, 24, 40, 11, 38, 40, 43, 98, 52, 52, 89, 14, 40, 39, 55, 51, 15, 62, 10, 71, 14, 55, 61, 57, 51, 21, 58, 35, 86, 60, 92, 68, 77, 0, 98, 55, 99, 69, 73, 89, 87, 27, 99, 37, 35, 95, 51, 92],
    [94, 51, 77, 91, 37, 42, 12, 80, 32, 97, 16, 20, 95, 90, 72, 60, 50, 41, 48, 58, 12, 97, 80, 44, 21, 51, 59, 33, 87, 86, 45, 47, 33, 23, 64, 68, 0, 54, 11, 23, 30, 26, 49, 77, 25, 85, 57, 41, 78, 71],
    [47, 86, 11, 51, 99, 54, 39, 74, 56, 23, 90, 17, 80, 36, 79, 83, 38, 42, 17, 24, 68, 23, 96, 37, 69, 44, 20, 47, 37, 19, 60, 16, 93, 39, 69, 62, 30, 0, 61, 63, 61, 47, 32, 64, 81, 54, 86, 27, 66, 67],
    [68, 42, 37, 70, 15, 36, 95, 45, 93, 66, 84, 49, 48, 42, 64, 68, 77, 18, 31, 74, 44, 66, 82, 10, 61, 18, 28, 26, 18, 14, 84, 69, 13, 15, 46, 77, 51, 99, 0, 17, 43, 93, 82, 34, 43, 62, 76, 31, 33, 38],
    [81, 43, 80, 19, 34, 74, 55, 92, 36, 52, 59, 31, 62, 87, 56, 29, 18, 27, 19, 25, 42, 60, 26, 96, 35, 74, 57, 35, 23, 18, 39, 51, 80, 95, 72, 29, 95, 51, 74, 0, 48, 75, 71, 50, 56, 65, 39, 35, 96, 61],
    [23, 73, 29, 64, 74, 97, 10, 20, 52, 63, 38, 84, 13, 60, 14, 78, 26, 52, 75, 18, 26, 88, 70, 55, 38, 63, 74, 92, 85, 60, 64, 45, 47, 36, 27, 65, 65, 87, 92, 11, 0, 32, 68, 76, 22, 95, 39, 44, 79, 43],
    [30, 31, 92, 66, 52, 84, 18, 30, 53, 82, 82, 97, 72, 57, 23, 16, 73, 21, 57, 69, 85, 61, 94, 62, 77, 60, 20, 39, 54, 86, 58, 33, 40, 12, 55, 38, 20, 96, 18, 46, 77, 0, 13, 11, 17, 41, 47, 50, 95, 18],
    [42, 20, 42, 41, 50, 72, 14, 40, 58, 66, 61, 89, 64, 51, 36, 99, 21, 76, 93, 36, 37, 36, 82, 28, 83, 84, 62, 36, 55, 70, 11, 21, 13, 39, 13, 13, 14, 86, 61, 53, 27, 61, 0, 36, 16, 70, 24, 31, 92, 63],
    [14, 15, 11, 88, 16, 90, 73, 41, 56, 47, 79, 11, 39, 52, 63, 89, 73, 61, 39, 94, 36, 27, 76, 98, 26, 75, 14, 51, 62, 73, 32, 23, 17, 67, 79, 18, 93, 97, 93, 26, 26, 63, 29, 0, 89, 49, 60, 47, 15, 87],
    [18, 72, 59, 64, 32, 65, 33, 18, 68, 63, 95, 78, 95, 77, 65, 95, 36, 61, 56, 70, 59, 70, 49, 70, 84, 58, 63, 13, 62, 65, 79, 44, 37, 71, 81, 32, 69, 19, 22, 57, 76, 59, 51, 46, 0, 10, 55, 49, 33, 34],
    [33, 25, 11, 91, 73, 12, 59, 46, 21, 88, 63, 19, 20, 44, 89, 14, 42, 89, 86, 35, 14, 29, 14, 25, 64, 89, 67, 46, 83, 91, 94, 59, 96, 22, 72, 77, 58, 23, 43, 47, 52, 43, 11, 91, 80, 0, 34, 88, 77, 84],
    [67, 30, 89, 15, 88, 23, 46, 90, 32, 87, 95, 74, 18, 30, 78, 26, 54, 17, 80, 27, 68, 86, 74, 40, 82, 63, 67, 16, 20, 14, 71, 55, 29, 64, 65, 81, 73, 29, 67, 29, 13, 49, 34, 21, 82, 81, 0, 68, 69, 88],
    [54, 90, 42, 83, 79, 95, 66, 24, 15, 17, 33, 40, 72, 13, 25, 69, 25, 22, 91, 81, 85, 61, 10, 14, 19, 34, 73, 11, 99, 31, 54, 69, 28, 54, 18, 45, 54, 35, 30, 15, 62, 69, 46, 31, 89, 39, 71, 0, 67, 90],
    [19, 41, 81, 20, 25, 67, 69, 15, 75, 44, 66, 63, 14, 42, 15, 44, 54, 32, 76, 51, 66, 59, 28, 89, 38, 58, 26, 89, 55, 81, 39, 87, 16, 30, 18, 43, 56, 98, 61, 53, 80, 47, 34, 48, 27, 12, 91, 20, 0, 62],
    [33, 67, 64, 75, 63, 17, 33, 87, 29, 65, 86, 32, 16, 42, 66, 89, 96, 39, 67, 94, 70, 15, 22, 20, 85, 31, 25, 41, 27, 24, 66, 71, 81, 88, 25, 37, 82, 60, 69, 59, 11, 80, 64, 38, 79, 20, 41, 15, 57, 0]
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

def cruzamento(p1, p2, ponto, n):
    d1 = np.concatenate((p1[0:ponto], p2[ponto:n]))
    d2 = np.concatenate((p2[0:ponto], p1[ponto:n]))
    return d1, d2


def mutacao2(d, n):
    pos1 = random.randrange(n)
    pos2 = random.randrange(n)
    d[pos1], d[pos2] = d[pos2], d[pos1]
    return d

def ajustaRestricao(desc, qd, corte, n):

    for i in range(qd):

        filho = list(desc[i])

        primeira_parte = set(filho[:corte])

        usados_segunda = set()
        repetidos = []

        for j in range(corte, n):

            gene = filho[j]

            if gene in primeira_parte:
                repetidos.append(j)

            elif gene in usados_segunda:
                repetidos.append(j)

            else:
                usados_segunda.add(gene)

        usados = primeira_parte.union(usados_segunda)

        faltantes = []

        for gene in range(n):
            if gene not in usados:
                faltantes.append(gene)

        random.shuffle(faltantes)

        for pos in repetidos:
            filho[pos] = faltantes.pop()

        desc[i] = np.array(filho)

    return desc

def gerarDescendentes(pop, fit, tp, n, tc, tm, metodo_selecao):
    qd = 2 * tp
    desc = np.zeros((qd, n), int)

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

def novaPopulacao(pop, desc, tp, ig):
    elite = int(ig * tp)
    nova = []
    for i in range(elite):
        nova.append(pop[i])
    for i in range(tp - elite):
        nova.append(desc[i])
    return nova

def algoritmoGenetico(
    matriz,
    tp,
    n,
    ng,
    tc,
    tm,
    ig,
    metodo_selecao='torneio',
    pop_inicial=None
):

    if pop_inicial is None:
        pop = popInicial(tp, n)
    else:
        pop = [ind.copy() for ind in pop_inicial]

    fit = [fitness(ind, matriz) for ind in pop]
    fit = normalizarFitness(fit)
    pop, fit = ordenar(pop, fit)

    melhor_inicial = pop[0].copy()

    for _ in range(ng):

        desc, qd, corte = gerarDescendentes(
            pop, fit, tp, n, tc, tm, metodo_selecao
        )

        desc = ajustaRestricao(desc, qd, corte, n)

        fit_desc = [fitness(ind, matriz) for ind in desc]
        fit_desc = normalizarFitness(fit_desc)

        desc, fit_desc = ordenar(desc, fit_desc)

        pop = novaPopulacao(pop, desc, tp, ig)

        fit = [fitness(ind, matriz) for ind in pop]
        fit = normalizarFitness(fit)

        pop, fit = ordenar(pop, fit)

    melhor_final = pop[0].copy()

    return (
        melhor_inicial,
        melhor_final,
        avaliar(n, melhor_inicial, matriz),
        avaliar(n, melhor_final, matriz)
    )

def gerarProblema(n):
    matriz = np.random.randint(low=10, high=100, size=(n, n))
    np.fill_diagonal(matriz, 0)
    return matriz

def individuoValido(ind, n):
    return len(ind) == n and len(set(ind)) == n and all(0 <= x < n for x in ind)

## Metodos usados para testar o funcionamento

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

def experimento_parametros():

    N = 50
    EXECUCOES = 20
    METODO_SELECAO = "torneio"

    matriz = matrizFixa

    TP = [10, 50, 100]
    NG = [10, 50, 100, 200]
    TC = [0.2, 0.5, 0.8]
    TM = [0.0, 0.2, 0.8]
    IG = [0.0, 0.1, 0.7]

    resultados = []

    configuracoes = list(itertools.product(TP, NG, TC, TM, IG))
    total_configuracoes = len(configuracoes)

    random.seed(42)
    np.random.seed(42)

    # Gera a maior população apenas uma vez
    pop_max = popInicial(max(TP), N)

    # Ordena a população pelo fitness para garantir
    # que o melhor indivíduo seja o mesmo em todos os testes
    fit_max = [fitness(ind, matriz) for ind in pop_max]
    fit_max = normalizarFitness(fit_max)

    pop_max, fit_max = ordenar(pop_max, fit_max)

    # Cria subconjuntos preservando o melhor indivíduo
    populacoes_fixas = {}

    for tp in TP:
        populacoes_fixas[tp] = [
            ind.copy() for ind in pop_max[:tp]
        ]

    for indice, (tp, ng, tc, tm, ig) in enumerate(configuracoes, start=1):

        print(
            f"[{indice}/{total_configuracoes}] "
            f"TP={tp} | NG={ng} | TC={tc} | TM={tm} | IG={ig}"
        )

        custos = []
        ganhos = []
        tempos = []

        melhor_inicial = None
        melhor_final = None
        custo_inicial = None

        for execucao in range(EXECUCOES):

            random.seed(execucao)
            np.random.seed(execucao)

            inicio_exec = time.perf_counter()

            sol_inicial, sol_final, custo_ini, custo_fin = algoritmoGenetico(
                matriz=matriz,
                tp=tp,
                n=N,
                ng=ng,
                tc=tc,
                tm=tm,
                ig=ig,
                metodo_selecao=METODO_SELECAO,
                pop_inicial=populacoes_fixas[tp]
            )

            fim_exec = time.perf_counter()

            tempos.append(fim_exec - inicio_exec)

            if melhor_inicial is None:
                melhor_inicial = sol_inicial.tolist()
                custo_inicial = custo_ini

            melhor_final = sol_final.tolist()

            custos.append(custo_fin)

            ganhos.append(
                ((custo_ini - custo_fin) / custo_ini) * 100
            )

        resultados.append({

            "TP": tp,
            "NG": ng,
            "TC": tc,
            "TM": tm,
            "IG": ig,

            "Custo Inicial": round(custo_inicial, 2),
            "Custo Médio": round(np.mean(custos), 2),
            "Melhor Custo": round(np.min(custos), 2),
            "Pior Custo": round(np.max(custos), 2),
            "Desvio Padrão": round(np.std(custos), 2),

            "Ganho Médio (%)": round(np.mean(ganhos), 2),
            "Tempo Médio (s)": round(np.mean(tempos), 4),

            "Solução Inicial": str(melhor_inicial),
            "Solução Final": str(melhor_final)
        })

    df = pd.DataFrame(resultados)

    df = df.sort_values(
        by=["Ganho Médio (%)", "Custo Médio"],
        ascending=[False, True]
    ).reset_index(drop=True)

    df.insert(0, "Ranking", df.index + 1)

    return df

if __name__ == "__main__":

    print("Iniciando experimentos...\n")

    inicio = time.perf_counter()

    df = experimento_parametros()

    fim = time.perf_counter()

    print("\nExperimentos concluídos.")

    print(df.head(20))

    print(f"\nTempo total: {fim - inicio:.2f} segundos")

    df.to_csv("resultados_ag.csv", index=False)

    df.to_excel(
        "resultados_ag.xlsx",
        index=False,
        engine="openpyxl"
    )

    print("\nArquivos salvos:")
    print("- resultados_ag.csv")
    print("- resultados_ag.xlsx")
