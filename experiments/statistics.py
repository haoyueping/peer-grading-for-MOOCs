#!/usr/bin/python3

from time import time

from scipy.stats import kendalltau

from algorithms.EM import em
from algorithms.PageRank import page_rank
from algorithms.borda_ordering import borda_ordering
from algorithms.random_circle_removal import random_circle_removal
from utils.gradings import get_gradings


def th(ranking, fraction):
    """The total number of correctly recovered relations between pairs that include an exam paper
    that is ranked in the top "fraction" in the ground truth. (Section 4.2)

    :param ranking: grading algorithm output
    :param fraction:
    :return:
    """
    limit = int(len(ranking) * fraction)
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


def acc(ranking, fraction):
    """The total number of correctly recovered relations between pairs with positions
    that differ by at least "fraction" in the ground truth. (Section 4.2)

    :param ranking: grading algorithm output
    :param fraction:
    :return:
    """
    rlen = len(ranking)
    gap = fraction * rlen
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
    # n, k, rep, algo, time, distance, ranking
    import pandas as pd

    rep = 10
    n = 1000
    k = 6
    algos = [random_circle_removal, page_rank, em, borda_ordering]
    algo_names = ['random_circle_removal', 'page_rank', 'em', 'borda_ordering']
    all2alls = [0 for x in algos]
    th10s = [0 for x in algos]
    th50s = [0 for x in algos]
    acc2s = [0 for x in algos]
    acc5s = [0 for x in algos]
    dataSet = []
    for i in range(rep):
        gradings = get_gradings(n, k)
        for j in range(len(algos)):
            start = time()
            ranking = algos[j](gradings)
            duration = time() - start
            dataSet.append(
                [n, k, i, algo_names[j], duration, kendalltau([x + 1 for x in range(n)], ranking)[0], str(ranking)])
            all2alls[j] += th(ranking, 1)
            th10s[j] += th(ranking, 0.1)
            th50s[j] += th(ranking, 0.5)
            acc2s[j] += acc(ranking, 0.02)
            acc5s[j] += acc(ranking, 0.05)
    all2alls = [x / rep for x in all2alls]
    th10s = [x / rep for x in th10s]
    th50s = [x / rep for x in th50s]
    acc2s = [x / rep for x in acc2s]
    acc5s = [x / rep for x in acc5s]

    df = pd.DataFrame(dataSet, columns=['n', 'k', 'rep', 'algo', 'time', 'distance', 'ranking'])
    df.to_csv('results.csv', index=False)
    print(all2alls)
    print(th10s)
    print(th50s)
    print(acc2s)
    print(acc5s)
