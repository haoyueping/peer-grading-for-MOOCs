#!/usr/bin/python3

import matplotlib.pyplot as plt

from algorithms.EM import em
from algorithms.PageRank import page_rank
from algorithms.borda_ordering import borda_ordering
from algorithms.random_circle_removal import random_circle_removal
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
    m = 10
    algos = [random_circle_removal, page_rank, em, borda_ordering]
    all2alls = [0 for x in algos]
    th10s = [0 for x in algos]
    th50s = [0 for x in algos]
    acc2s = [0 for x in algos]
    acc5s = [0 for x in algos]
    for i in range(m):
        for j in range(len(algos)):
            ranking = algos[j](gradings)
            all2alls[j] += th(ranking, 1)
            th10s[j] += th(ranking, 0.1)
            th50s[j] += th(ranking, 0.5)
            acc2s[j] += acc(ranking, 0.02)
            acc5s[j] += acc(ranking, 0.05)
    all2alls = [x / m for x in all2alls]
    th10s = [x / m for x in th10s]
    th50s = [x / m for x in th50s]
    acc2s = [x / m for x in acc2s]
    acc5s = [x / m for x in acc5s]

    print(all2alls)
    print(th10s)
    print(th50s)
    print(acc2s)
    print(acc5s)
