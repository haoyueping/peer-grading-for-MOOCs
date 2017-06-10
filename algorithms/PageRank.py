import numpy as np
import pandas as pd
from scipy.stats import kendalltau

from utils.gradings import get_gradings


def page_rank(short_rankings):
    n, k = short_rankings.shape
    P = np.zeros((n, n))
    for ranking in short_rankings:
        for i in range(k):
            for j in range(i + 1, k):
                better_paper = ranking[i]
                worse_paper = ranking[j]
                P[worse_paper - 1][better_paper - 1] += 1

    P += (np.ones_like(P) - np.eye(n)) / n
    P /= P.sum(axis=1)[:, None]

    print('new round.')
    while True:
        P_temp = str(P)
        P = P.dot(P)
        P /= P.sum(axis=1)[:, None]
        if P_temp == str(P):
            break

    global_scores = pd.Series(P[0])
    global_ranking = np.array(global_scores.sort_values(ascending=False).index) + 1
    return global_ranking


if __name__ == '__main__':
    n = 1000
    truth_ranking = list(range(1, n + 1))

    # rankings = np.genfromtxt('../data/data_n_{}_k_6.csv'.format(n), delimiter=',', dtype='int')
    rankings = get_gradings(n, 34)
    from time import time

    t = time()
    global_ranking = page_rank(rankings)
    print('time = {}'.format(time() - t))
    accuracy = kendalltau(truth_ranking, global_ranking)
    print(accuracy)
