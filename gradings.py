# coding: utf-8
from bundle_graph import create_bundle_graph
from random import uniform
from numpy.random import choice
import numpy as np

def probability_distribution_for_inserting_jth_item(j, p):
    probs = np.array([p**(j-i) for i in range(j+1)])
    return probs / probs.sum()

def randomize_complete_ranking(ranking):
    k = len(ranking)
    r = []
    for i in range(k):
        pos = choice(list(range(i+1)), p=probability_distribution_for_inserting_jth_item(i, uniform(0, 0.5)))
        r.insert(pos, i)
    return r

def get_gradings(n, k):
    indices = np.empty((n, k))
    indices = np.apply_along_axis(randomize_complete_ranking, 1, indices)

    students = create_bundle_graph(n, k)
    bundles = np.empty((n,k))
    for idx, student in enumerate(students):
        bundles[idx] = sorted(student.papers)

    rankings = np.empty_like(indices)
    for i in range(n):
        for j in range(k):
            rankings[i][j] = bundles[i][indices[i][j]]

    return rankings

if __name__ == '__main__':

    import random

    random.seed(1)
    np.random.seed(1)

    import pandas as pd

    n = 1000
    k = 6

    gradings = get_gradings(n, k)
    print(gradings)
    df = pd.DataFrame(gradings)
    df.to_csv("data_n_1000_k_6.csv", index=False)