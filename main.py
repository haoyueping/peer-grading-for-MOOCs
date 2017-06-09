#!/usr/bin/python3

from time import time

import pandas as pd
from scipy.stats import kendalltau

from algorithms.EM import em
from algorithms.PageRank import page_rank
from algorithms.borda_ordering import borda_ordering
from algorithms.random_circle_removal import random_circle_removal
from utils.gradings import get_gradings


def experiment(n, k_list, repetition):
    algos = [random_circle_removal, page_rank, em, borda_ordering]
    algo_names = ['random_circle_removal', 'page_rank', 'em', 'borda_ordering']

    file_name = './out/results_n_{}_k_{}.csv'.format(n, str(k_list))
    myfile = open(file_name, 'w')
    myfile.write('n, k, rep, algo, time, distance, ranking\n')
    for rep in range(repetition):
        for k in k_list:
            gradings = get_gradings(n, k)
            for j in range(len(algos)):
                start = time()
                ranking = algos[j](gradings)
                duration = time() - start
                line = '{},{},{},{},{},{}'.format(n, k, rep, algo_names[j], duration,
                                         kendalltau(list(range(1, n + 1)), ranking)[0])
                myfile.write(line)
                myfile.write(',[')
                for item in ranking[:-1]:
                    myfile.write('{},'.format(item))
                myfile.write('{}]\n'.format(ranking[-1]))

    myfile.close()



if __name__ == '__main__':
    repetition = 2
    n = 10000
    k_list = [6, 8]

    experiment(n, k_list, repetition)
