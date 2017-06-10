#!/usr/bin/python3

import matplotlib.pyplot as plt
import numpy as np

from algorithms.EM import em
from algorithms.PageRank import page_rank
from algorithms.borda_ordering import borda_ordering
from algorithms.random_circle_removal import random_circle_removal
from utils.gradings import get_gradings

def position_displacement(rankings):
    result = np.array([0 for x in range(len(rankings[0]))])
    ground_truth = np.array([x + 1 for x in range(len(rankings[0]))])
    for ranking in rankings:
        ranking = np.array(ranking)
        result += ground_truth - ranking
    result = result / len(rankings)
    return ground_truth, result

def display(x, ys, algo_names, id):
    plt.figure(id)
    bar_width = 1
    alpha = 0.4

    colors = ['b', 'g', 'r']
    for i in range(len(ys)):
        plt.scatter(x + (bar_width * i), ys[i].tolist(), bar_width, color = colors[i], alpha = alpha, label=algo_names[i])
    plt.legend()
    plt.ylabel('Average Displacement')
    plt.xlabel('Ground Truth Ranking')
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    k = [6]
    n = 10000
    m = 500
    result = np.genfromtxt('out/large/results_n_{}_k_{}.csv'.format(n, str(k)), delimiter=',', dtype='str', skip_header=1)
    start = 6

    ranking_algo = ['page_rank', 'em', 'borda']
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

    ys = []
    x, y = position_displacement(rankings_pr)
    ys.append(y)
    x, y = position_displacement(rankings_em)
    ys.append(y)
    x, y = position_displacement(rankings_borda)
    ys.append(y)
    display(x, ys, ranking_algo, 1)
