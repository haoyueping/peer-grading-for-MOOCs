#!/usr/bin/python3

import matplotlib.pyplot as plt

from algorithms.EM import em
from algorithms.PageRank import page_rank
from algorithms.borda_ordering import borda_ordering
from utils.gradings import get_gradings
from datetime import datetime

def complexity(algorithm, ranking, m):
    time = 0
    for i in range(m):
        start = datetime.now()
        algorithm(ranking)
        end = datetime.now()
        time += (end - start).total_seconds()
    return time / m

def display(x, y, id):
    plt.figure(id)
    ranking_algo = ['em', 'borda']

    handles = []
    for i in range(len(y)):
        line, = plt.plot(x, y[i], label = ranking_algo[i])
        handles.append(line)
    plt.legend(handles = handles)
    plt.ylabel('time(second)')
    plt.xlabel('numnber of student')
    plt.show()

if __name__ == '__main__':
    m = 10
    n = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
    k = 6

    algos = [em, borda_ordering]
    all_times = []
    for algo in algos:
        times = []
        for i in n:
            gradings = get_gradings(i, k)
            times.append(complexity(algo, gradings, m));
        all_times.append(times);
    display(n, all_times, 1)
