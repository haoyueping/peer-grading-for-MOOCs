from numpy.random import choice
from scipy.stats import kendalltau
import numpy as np
import pandas as pd


def borda_ordering_of_global_ranks(rankings, scores):
    n, k = rankings.shape
    borda_scores = np.zeros(n)
    for ranking, ranks in zip(rankings, scores):
        for paper, rank in zip(ranking, ranks):
            borda_scores[paper - 1] += rank

    borda_scores = pd.Series(borda_scores)
    borda_ranking = np.array(borda_scores.sort_values().index, dtype='int') + 1
    return borda_ranking


def probability_distribution_for_inserting_jth_item(j, p):
    probs = np.array([p ** (j - i) for i in range(j + 1)])
    return probs / probs.sum()


def mallows_posterior(global_ranking, short_ranking, phi=0.25):
    papers = set(short_ranking)
    ranks = np.arange(0, len(short_ranking), 1, dtype='int')
    for idx, paper in enumerate(global_ranking):
        if paper not in papers:
            pos = choice(list(range(idx + 1)), p=probability_distribution_for_inserting_jth_item(idx, phi))
            local_pos = np.searchsorted(ranks, pos)
            for local_idx in range(local_pos, len(ranks)):
                ranks[local_idx] += 1

    return ranks


def update_scores_by_global_ranking(rankings, scores, global_ranking):
    for idx, ranking in enumerate(rankings):
        scores[idx] = np.where(np.in1d(global_ranking, ranking))[0]
    return scores


def EM(rankings):
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

    global_ranking = EM(rankings)
    print(kendalltau(truth_ranking, global_ranking))
