import numpy as np
import pandas as pd
from scipy.stats import kendalltau

from utils.gradings import get_gradings


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
        # print(kendalltau(truth_ranking, global_ranking))
        if temp == str(global_ranking):
            break
    return global_ranking


if __name__ == '__main__':
    n = 1000
    truth_ranking = list(range(1, n + 1))
    # rankings = np.genfromtxt('../data/data_n_{}_k_6.csv'.format(n), delimiter=',', dtype='int')
    rankings = get_gradings(n, 34)

    from time import time

    t = time()
    global_ranking = em(rankings)
    print('time = {}'.format(time() - t))
    accuracy = kendalltau(truth_ranking, global_ranking)
    print(accuracy)
