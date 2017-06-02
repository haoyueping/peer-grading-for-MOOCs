#!/usr/bin/python3

import matplotlib.pyplot as plt

from algorithms.EM import em
from algorithms.PageRank import page_rank
from algorithms.borda_ordering import borda_ordering
from algorithms.random_circle_removal import random_circle_removal
from algorithms.weighted_graph import weighted_graph
from utils.gradings import get_gradings


def th(ranking, th):
    limit = int(len(ranking) * th)
    rlen = len(ranking)

    cnt = 0
    total = 0
    for i in range(rlen):
        for j in range(i + 1, rlen):
            if (ranking[i] < limit) or (ranking[j] < limit):
                total += 1
                if ranking[i] < ranking[j]:
                    cnt += 1
    return cnt / total


def acc(ranking, acc):
    rlen = len(ranking)
    gap = acc * rlen
    cnt = 0
    total = 0
    for i in range(rlen):
        for j in range(i + 1, rlen):
            if abs(ranking[i] - ranking[j]) >= gap:
                total = total + 1
                if ranking[i] < ranking[j]:
                    cnt = cnt + 1
    return cnt / total

def display(x, y, xlabel, ylabel, axis, id):
    plt.figure(id)

    plt.plot(x, y, 'bx')
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.axis(axis)
    plt.show()

if __name__ == '__main__':
    gradings = get_gradings(1000, 6)
    all2all = []
    th10 = []
    th50 = []
    acc2 = []
    acc5 = []

    ranking = random_circle_removal(gradings)
    all2all.append(th(ranking, 1))
    th10.append(th(ranking, 0.1))
    th50.append(th(ranking, 0.5))
    acc2.append(acc(ranking, 0.02))
    acc5.append(acc(ranking, 0.05))

    ranking = page_rank(gradings)
    all2all.append(th(ranking, 1))
    th10.append(th(ranking, 0.1))
    th50.append(th(ranking, 0.5))
    acc2.append(acc(ranking, 0.02))
    acc5.append(acc(ranking, 0.05))

    ranking = em(gradings)
    all2all.append(th(ranking, 1))
    th10.append(th(ranking, 0.1))
    th50.append(th(ranking, 0.5))
    acc2.append(acc(ranking, 0.02))
    acc5.append(acc(ranking, 0.05))

    ranking = borda_ordering(gradings)
    all2all.append(th(ranking, 1))
    th10.append(th(ranking, 0.1))
    th50.append(th(ranking, 0.5))
    acc2.append(acc(ranking, 0.02))
    acc5.append(acc(ranking, 0.05))

    ranking = weighted_graph();
    all2all.append(th(ranking, 1))
    th10.append(th(ranking, 0.1))
    th50.append(th(ranking, 0.5))
    acc2.append(acc(ranking, 0.02))
    acc5.append(acc(ranking, 0.05))

    print(all2all)
    print(th10)
    print(th50)
    print(acc2)
    print(acc5)

    # all2all_rcr = []
    # th10_rcr = []
    # acc5_rcr = []
    #
    # all2all_pr = []
    # th10_pr = []
    # acc5_pr = []
    #
    # all2all_em = []
    # th10_em = []
    # acc5_em = []
    #
    # all2all_borda = []
    # th10_borda = []
    # acc5_borda = []
    #
    # k = 100
    # for i in range(k):
    #     print(i)
    #     gradings = get_gradings(1000, 6)
    #
    #     ranking = random_circle_removal(gradings)
    #     all2all_rcr.append(th(ranking, 1))
    #     th10_rcr.append(th(ranking, 0.1))
    #     acc5_rcr.append(acc(ranking, 0.05))
    #
    #     ranking = borda_ordering(gradings)
    #     all2all_borda.append(th(ranking, 1));
    #     th10_borda.append(th(ranking, 0.1))
    #     acc5_borda.append(acc(ranking, 0.05))
    #
    #     ranking = page_rank(gradings)
    #     all2all_pr.append(th(ranking, 1));
    #     th10_pr.append(th(ranking, 0.1))
    #     acc5_pr.append(acc(ranking, 0.05))
    #
    #     ranking = em(gradings)
    #     all2all_em.append(th(ranking, 1))
    #     th10_em.append(th(ranking, 0.1))
    #     acc5_em.append(acc(ranking, 0.05))
    #
    # rcr_borda = [[all2all_rcr, all2all_borda, 'rcr_all2all', 'borda_all2all', [0.88, 0.9, 0.41, 0.43]],
    #     [th10_rcr, th10_borda, 'rcr_th10', 'borda_th10', [0.95, 0.97, 0.40, 0.42]],
    #     [acc5_rcr, acc5_borda, 'rcr_acc5', 'borda_acc5', [0.91, 0.93, 0.41, 0.43]]]
    # pr_borda = [[all2all_pr, all2all_borda, 'pr_all2all', 'borda_all2all', [0.88, 0.9, 0.84, 0.86]],
    #     [th10_pr, th10_borda, 'pr_th10', 'borda_th10', [0.95, 0.97, 0.90, 0.92]],
    #     [acc5_pr, acc5_borda, 'pr_acc5', 'borda_acc5', [0.91, 0.93, 0.88, 0.90]]]
    # em_borda = [[all2all_em, all2all_borda, 'em_all2all', 'borda_all2all', [0.88, 0.9, 0.86, 0.88]],
    #     [th10_em, th10_borda, 'em_th10', 'borda_th10', [0.95, 0.97, 0.92, 0.94]],
    #     [acc5_em, acc5_borda, 'em_acc5', 'borda_acc5', [0.91, 0.93, 0.90, 0.92]]]
    # cmp = [rcr_borda, pr_borda, em_borda]
    #
    # id = 1
    # for comparisons in cmp:
    #     for comparison in comparisons:
    #         display(comparison[1], comparison[0], comparison[3], comparison[2], comparison[4], id)
    #         id += 1
