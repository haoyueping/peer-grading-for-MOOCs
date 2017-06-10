import numpy as np
import pandas as pd
from scipy.stats import kendalltau

from utils.gradings import get_gradings


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
    n = 1000
    truth_ranking = list(range(1, n + 1))
    # rankings = np.genfromtxt('../data/data_n_{}_k_6.csv'.format(n), delimiter=',', dtype='int')
    rankings = get_gradings(n, 34)

    from time import time

    t = time()
    global_ranking = borda_ordering(rankings)
    print('time = {}'.format(time() - t))
    accuracy = kendalltau(truth_ranking, global_ranking)
    print(accuracy)
