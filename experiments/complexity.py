#!/usr/bin/python3

from datetime import datetime

import matplotlib.pyplot as plt

from algorithms.EM import em
from algorithms.borda_ordering import borda_ordering
from utils.gradings import get_gradings


def complexity(algorithm, ranking):
    start = datetime.now()
    algorithm(ranking)
    end = datetime.now()
    return (end - start).total_seconds()


def displayAggregated(x, times, id):
    algo_names = ['borda', 'em']
    y = []
    for algo in algo_names:
        df = times.loc[times['algorithm'] == algo]
        t = df.groupby('n').mean()['time'].tolist()
        y.append(t)

    plt.figure(id)
    handles = []
    for i in range(len(y)):
        line, = plt.plot(x, y[i], label=algo_names[i])
        handles.append(line)
    plt.legend(handles=handles)
    plt.ylabel('time(second)')
    plt.xlabel('number of student')
    plt.show()


def displayScattered(times, id):
    plt.figure(id)

    algo_names = ['borda', 'em']
    for algo in algo_names:
        df = times.loc[times['algorithm'] == algo]
        plt.scatter(df['n'], df['time'], label=algo)

    plt.legend()
    plt.ylabel('time(second)')
    plt.xlabel('numnber of student')
    plt.show()


if __name__ == '__main__':
    import pandas as pd

    m = 2
    n = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
    k = 6

    a = 2  # len(n)

    algos = [borda_ordering, em]
    algo_names = ['borda', 'em']
    all_times = []
    times = pd.DataFrame(columns=['algorithm', 'n', 'repetition', 'time'])
    for i in n[:a]:
        for j in range(m):
            gradings = get_gradings(i, k)
            for algo, algo_name in zip(algos, algo_names):
                print(i, j, algo_name)
                times.loc[times.index.size] = [algo_name, i, j, complexity(algo, gradings)]

    displayScattered(times, 1)
    displayAggregated(n[:a], times, 2)
