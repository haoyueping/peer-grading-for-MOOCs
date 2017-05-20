#!/usr/bin/python3

from random_circle_removal import random_circle_removal
from gradings import get_gradings
from PageRank import page_rank
from EM import em
from borda_ordering import borda_ordering

def th(ranking, th):
    limit = int(len(ranking) * th)
    ranking = list(filter(lambda x: x <= limit, ranking))
    rlen = len(ranking)
    cnt = 0
    total = 0

    for i in range(rlen):
        for j in range(i + 1, rlen):
            total = total + 1
            if ranking[i] < ranking[j]:
                cnt = cnt + 1
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

    print(all2all)
    print(th10)
    print(th50)
    print(acc2)
    print(acc5)
