#!/usr/bin/python3

import matplotlib.pyplot as plt

from algorithms.EM import em
from algorithms.PageRank import page_rank
from algorithms.borda_ordering import borda_ordering
from algorithms.random_circle_removal import random_circle_removal
from algorithms.weighted_graph import weighted_graph
from utils.gradings import get_gradings

n = 1000
k = 6
ranking_algo = ['random_circle_removal', 'page_rank', 'em', 'borda', 'weighted_graph']

def displacement(rankings):
    displacement_percentage = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6]
    displacements = []

    for ranking in rankings:
        number = {percentage: 0 for percentage in displacement_percentage}
        for i in range(1, n + 1):
            for percentage in displacement_percentage:
                if abs(ranking[i - 1] - i) / n >= percentage:
                    number[percentage] += 1
        displacements.append([number[p] / n for p in displacement_percentage])

    return displacement_percentage, displacements

def interval_displacement(rankings):
    plt.figure(2)
    displacement_percentage = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]
    displacements = []

    for ranking in rankings:
        number = {percentage: 0 for percentage in displacement_percentage}
        for j in range(len(displacement_percentage)):
            s = set(ranking[0: int(displacement_percentage[j] * n)])
            for i in range(1, n + 1):
                if i > displacement_percentage[j] * n:
                    break
                if i in s:
                    number[displacement_percentage[j]] += 1
        displacements.append([number[p] / (n * p) for p in displacement_percentage])

    return displacement_percentage, displacements

def distribution20(rankings):
    plt.figure(3)
    interval_percentage = [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75]
    distributions = []

    for ranking in rankings:
        r = set(ranking[0: int(n * 0.2)])
        number = {percentage: 0 for percentage in interval_percentage}
        for i in interval_percentage:
            for j in range(int(n * (i - 0.05) + 1), int(n * i + 1)):
                if j in r:
                    number[i] += 1
        distributions.append([number[p] / (n * 0.05) for p in interval_percentage])

    return interval_percentage, distributions

def display(x, y, id):
    plt.figure(id)

    handles = []
    for i in range(len(y)):
        line, = plt.plot(x, y[i], marker = 'o', label = ranking_algo[i])
        handles.append(line)
    plt.legend(handles = handles)
    plt.ylabel('Fraction of students displaced')
    plt.xlabel('Fraction of position displaced')
    plt.show()

if __name__ == '__main__':
    gradings = get_gradings(n, k)
    ranking_rcr = random_circle_removal(gradings)
    ranking_pr = page_rank(gradings)
    ranking_em = em(gradings)
    ranking_b = borda_ordering(gradings)
    ranking_wg = weighted_graph()
    rankings = [ranking_rcr, ranking_pr, ranking_em, ranking_b, ranking_wg]

    x, y = displacement(rankings)
    display(x, y, 1)
    x, y = interval_displacement(rankings)
    display(x, y, 2)
    x, y = distribution20(rankings)
    display(x, y, 3)
