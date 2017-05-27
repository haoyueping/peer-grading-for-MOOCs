from random import random
import numpy as np
import pandas as pd
from scipy.stats import kendalltau


def borda_ordering_of_global_ranks(rankings, scores):
    n, k = rankings.shape
    borda_scores = np.zeros(n)
    for ranking, ranks in zip(rankings, scores):
        for paper, rank in zip(ranking, ranks):
            borda_scores[paper - 1] += rank

    borda_scores = pd.Series(borda_scores)
    borda_ranking = np.array(borda_scores.sort_values().index, dtype='int') + 1
    return borda_ranking


def update_scores_by_global_ranking(rankings, scores, global_ranking):
    for idx, ranking in enumerate(rankings):
        scores[idx] = np.where(np.in1d(global_ranking, ranking))[0]
    return scores

# def update_scores_by_global_ranking(rankings, scores, global_ranking):
#     for idx, ranking in enumerate(rankings):
#
#         positions = []
#         full_ranking = list(global_ranking)
#         for paper in ranking:
#             positions.append(full_ranking.index(paper))
#
#         # print(kendalltau(positions, list(range(len(positions))))[0])
#         if 0.7 > kendalltau(positions, list(range(len(positions))))[0]:
#             scores[idx] = positions
#         else:
#             scores[idx] = np.where(np.in1d(global_ranking, ranking))[0]
#     return scores


def em(rankings):
    n, k = rankings.shape
    scores = np.tile(list(range(k)), (n, 1)) + 1
    global_ranking = borda_ordering_of_global_ranks(rankings, scores)
    while True:
        temp = str(global_ranking)
        scores = update_scores_by_global_ranking(rankings, scores, global_ranking)
        global_ranking = borda_ordering_of_global_ranks(rankings, scores)
        print(kendalltau(truth_ranking, global_ranking))
        if temp == str(global_ranking):
            break
    return global_ranking


if __name__ == '__main__':
    truth_ranking = list(range(1, 1000 + 1))
    rankings = np.genfromtxt('data_n_1000_k_6.csv', delimiter=',', dtype='int')

    global_ranking = em(rankings)
    print(kendalltau(truth_ranking, global_ranking))
