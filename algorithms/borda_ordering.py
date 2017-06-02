import numpy as np
import pandas as pd
from scipy.stats import kendalltau


def borda_ordering(rankings):
    n, k = rankings.shape
    borda_scores = np.zeros(n)
    for ranking in rankings:
        for idx, paper in enumerate(ranking):
            borda_scores[paper - 1] += idx + 1

    borda_scores = pd.Series(borda_scores)
    borda_ranking = np.array(borda_scores.sort_values().index, dtype='int') + 1
    return borda_ranking


if __name__ == '__main__':
    truth_ranking = list(range(1, 1000 + 1))
    rankings = np.genfromtxt('data/data_n_1000_k_6.csv', delimiter=',', dtype='int')

    global_ranking = borda_ordering(rankings)
    res = kendalltau(global_ranking, truth_ranking)
    print(res)
