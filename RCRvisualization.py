#!/usr/bin/python3

import sys
from datetime import datetime
import matplotlib.pyplot as plt
from bundle_graph import create_bundle_graph
from RCRranking import rcrranking
from scipy import stats

if __name__ == '__main__':
    fig = sys.argv[1]
    if fig == 'n':
        n = [100, 250, 500, 750, 1000, 1250, 1500, 1750, 2000]
        k = [6, 6, 6, 6, 6, 6, 6, 6, 6]
        time_n = []

        for i in range(len(n)):
            start = datetime.now()
            create_bundle_graph(n[i], k[i])
            time_n.append((datetime.now() - start).total_seconds())
        plt.plot(time_n, n)
        plt.ylabel('with k fixed to 6')
        plt.show()
    elif fig == 'k':
        n = [500, 500, 500, 500, 500, 500, 500]
        k = [2, 4, 6, 8, 10, 12, 14]
        time_k = []

        for i in range(len(n)):
            start = datetime.now()
            create_bundle_graph(n[i], k[i])
            time_k.append((datetime.now() - start).total_seconds())

        plt.plot(time_k, k)
        plt.ylabel('with n fixed to 500')
        plt.show()
    elif fig == 'correctness-n':
        n = [100, 250, 500, 750, 1000]
        k = [6, 6, 6, 6, 6]
        correctness_n = []

        for i in range(len(n)):
            ground_truth = [x + 1 for x in range(n[i])]
            ranking = rcrranking(n[i], k[i])
            tau, p_value = stats.kendalltau(ranking, ground_truth)
            correctness_n.append(tau)
        plt.plot(n, correctness_n)
        plt.ylabel('with k fixed to 6')
        plt.show()

    elif fig == 'correctness-k':
        n = [500, 500, 500, 500, 500]
        k = [2, 4, 6, 8, 10]
        correctness_k = []

        for i in range(len(n)):
            ground_truth = [x + 1 for x in range(n[i])]
            ranking = rcrranking(n[i], k[i])
            tau, p_value = stats.kendalltau(ranking, ground_truth)
            correctness_k.append(tau)
        plt.plot(k, correctness_k)
        plt.ylabel('with n fixed to 500')
        plt.show()
