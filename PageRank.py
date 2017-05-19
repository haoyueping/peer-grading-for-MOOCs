import numpy as np
import pandas as pd
from numpy.linalg import matrix_power
from scipy.stats import kendalltau


def page_rank(short_rankings):
    n, k = short_rankings.shape

    P = np.zeros((n, n))
    for ranking in short_rankings:
        for i in range(k-1):
            better_paper = ranking[i]
            worse_paper = ranking[i+1]
            P[worse_paper - 1][better_paper - 1] += 1

    P_super = np.ones_like(P) / n
    P_super -= np.eye(n) / n

    P_final = P + P_super
    for i in range(n):
        P_final[i] = P_final[i] / P_final[i].sum()

    while True:
        P_temp = str(P_final)
        P_final = matrix_power(P_final, 10)
        if P_temp == str(P_final):
            break

    global_scores = pd.Series(P_final[0])
    global_ranking = np.array(global_scores.sort_values(ascending=False).index) + 1
    return global_ranking


if __name__ == '__main__':
    truth_ranking = list(range(1, 1000 + 1))

    rankings = np.genfromtxt('data_n_1000_k_6.csv', delimiter=',', dtype='int')
    global_ranking = page_rank(rankings)

    accuracy = kendalltau(truth_ranking, global_ranking)
    print(accuracy)
