#!/usr/bin/python3

import sys

import matplotlib.pyplot as plt
import numpy as np

from algorithms.EM import em
from algorithms.PageRank import page_rank
from algorithms.borda_ordering import borda_ordering
from algorithms.random_circle_removal import random_circle_removal
from utils.gradings import get_gradings

ranking_algo = ['Random Walk', 'EM', 'Border Score']


def displacement(rankings, n, m):
    displacement_percentage = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6]
    displacements = []

    for ranking_set in rankings:
        temp = [0 for x in displacement_percentage]
        for ranking in ranking_set:
            number = {percentage: 0 for percentage in displacement_percentage}
            for i in range(1, n + 1):
                for percentage in displacement_percentage:
                    if abs(ranking[i - 1] - i) / n >= percentage:
                        number[percentage] += 1
            for p in range(len(displacement_percentage)):
                temp[p] += number[displacement_percentage[p]] / n
        temp = [x / m for x in temp]
        displacements.append(temp)
    return displacement_percentage, displacements


def interval_displacement(rankings, n, m):
    displacement_percentage = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8,
                               0.85, 0.9, 0.95, 1]
    displacements = []

    for ranking_set in rankings:
        temp = [0 for x in displacement_percentage]
        for ranking in ranking_set:
            number = {percentage: 0 for percentage in displacement_percentage}
            for j in range(len(displacement_percentage)):
                s = set(ranking[0: int(displacement_percentage[j] * n)])
                for i in range(1, n + 1):
                    if i > displacement_percentage[j] * n:
                        break
                    if i in s:
                        number[displacement_percentage[j]] += 1
            for p in range(len(displacement_percentage)):
                temp[p] += number[displacement_percentage[p]] / (n * displacement_percentage[p])
        temp = [x / m for x in temp]
        displacements.append(temp)

    return displacement_percentage, displacements


def distribution20(rankings, n, m):
    interval_percentage = [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75]
    distributions = []

    for ranking_set in rankings:
        temp = [0 for x in interval_percentage]
        for ranking in ranking_set:
            r = set(ranking[0: int(n * 0.2)])
            number = {percentage: 0 for percentage in interval_percentage}
            for i in interval_percentage:
                for j in range(int(n * (i - 0.05) + 1), int(n * i + 1)):
                    if j in r:
                        number[i] += 1
            for p in range(len(interval_percentage)):
                temp[p] += number[interval_percentage[p]] / (n * 0.05)
        temp = [x / m for x in temp]
        distributions.append(temp)

    return interval_percentage, distributions


def display(x, y, id):
    plt.figure(id)

    handles = []
    for i in range(len(y)):
        line, = plt.plot(x, y[i], marker='o', label=ranking_algo[i])
        handles.append(line)
    plt.legend(handles=handles)
    plt.ylabel('Fraction of students displaced')
    plt.xlabel('Fraction of position displaced')
    plt.show()


if __name__ == '__main__':
    k = [6]
    n = 10000
    m = 10
    result = np.genfromtxt('out/large/results_n_{}_k_{}.csv'.format(n, str(k)), delimiter=',', dtype='str', skip_header=1)
    start = 6

    rankings_pr = []
    rankings_em = []
    rankings_borda = []
    for i in range(0, m * 3, 3):
        ranking = []
        for j in range(start, n + start):
            ranking.append(int(result[i][j]))
        rankings_pr.append(ranking)
        ranking = []
        for j in range(start, n + start):
            ranking.append(int(result[i + 1][j]))
        rankings_em.append(ranking)
        ranking = []
        for j in range(start, n + start):
            ranking.append(int(result[i + 2][j]))
        rankings_borda.append(ranking)
    rankings = [rankings_pr, rankings_em, rankings_borda]
    x, y = displacement(rankings, n, m)
    display(x, y, 1)
    x, y = interval_displacement(rankings, n, m)
    display(x, y, 2)
    x, y = distribution20(rankings, n, m)
    display(x, y, 3)
