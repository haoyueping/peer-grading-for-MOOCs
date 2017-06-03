#!/usr/bin/python3

import matplotlib.pyplot as plt
import sys

from algorithms.EM import em
from algorithms.PageRank import page_rank
from algorithms.borda_ordering import borda_ordering
from algorithms.random_circle_removal import random_circle_removal
from utils.gradings import get_gradings

ranking_algo = ['random_circle_removal', 'page_rank', 'em', 'borda']

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
    displacement_percentage = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]
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
        line, = plt.plot(x, y[i], marker = 'o', label = ranking_algo[i])
        handles.append(line)
    plt.legend(handles = handles)
    plt.ylabel('Fraction of students displaced')
    plt.xlabel('Fraction of position displaced')
    plt.show()

if __name__ == '__main__':
    test_type = sys.argv[1]
    n = int(sys.argv[2])
    k = int(sys.argv[3])
    m = int(sys.argv[4])
    which = sys.argv[5]
    gradings = get_gradings(n, k)
    rankings = []
    if test_type == 'em_borda':
        ranking_algo = ['em', 'borda']
        rankings_em = []
        rankings_borda = []

        for i in range(m):
            rankings_em.append(em(gradings))
            rankings_borda.append(borda_ordering(gradings))
        rankings.append(rankings_em)
        rankings.append(rankings_borda)
    elif test_type == 'regular':
        rankings_rcr = []
        rankings_pr = []
        rankings_em = []
        rankings_borda = []

        for i in range(m):
            if n <= 1000:
                rankings_rcr.append(random_circle_removal(gradings))
                rankings_pr.append(page_rank(gradings))
            rankings_em.append(em(gradings))
            rankings_borda.append(borda_ordering(gradings))
        if n <= 1000:
            rankings.append(rankings_rcr)
            rankings.append(rankings_pr)
        rankings.append(rankings_em)
        rankings.append(rankings_borda)

    if which == '1':
        x, y = displacement(rankings, n, m)
        display(x, y, 1)
    elif which == '2':
        x, y = interval_displacement(rankings, n, m)
        display(x, y, 2)
    elif which == '3':
        x, y = distribution20(rankings, n, m)
        display(x, y, 3)
    elif which == 'all':
        x, y = displacement(rankings, n, m)
        display(x, y, 1)
        x, y = interval_displacement(rankings, n, m)
        display(x, y, 2)
        x, y = distribution20(rankings, n, m)
        display(x, y, 3)
