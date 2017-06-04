import itertools
import time

import numpy as np
import scipy
import scipy.misc
import scipy.stats


# import pyximport; pyximport.install()
# import find_c


def N_of_sigma(sigma, k):
    h = np.asarray(sigma, dtype='int')
    freq, bins = np.histogram(h, np.arange(k + 1))
    fact = scipy.misc.factorial(freq)
    return np.math.factorial(k) / np.prod(fact)


def nCr(n, r):
    return np.math.factorial(n) / np.math.factorial(r) / np.math.factorial(n - r)


def find_c(sigma, k, P):
    c = np.zeros(k ** 2 - k + 1)
    for l1 in range(1, k + 1):
        for l2 in range(1, k + 1):
            print(l1, l2)
            for l3 in range(1, k + 1):
                for l4 in range(1, k + 1):
                    for l5 in range(1, k + 1):
                        for l6 in range(1, k + 1):
                            l = np.array([l1, l2, l3, l4, l5, l6])
                            suml = l.sum()
                            for j in range(k ** 2 - suml + 1):
                                temp = 1.0
                                for i in range(1, k + 1):
                                    temp = temp * P[sigma[i - 1], l[i - 1] - 1] * nCr(k - 1, l[i - 1] - 1)
                                c[suml - k + j] = c[suml - k + j] + N_of_sigma(sigma, k) * temp * nCr(k ** 2 - suml,
                                                                                                      j) * ((-1) ** j)

    return c


def find_d(sigma_prime, c_prime, k, P, perf_tuple):
    d = np.zeros(k ** 2 - k + 2)
    for s in range(k ** 2 - k):
        d[0] += (c_prime[s] * (perf_tuple[3] ** (s + 1))) / (s + 1)

    for s in range(1, k ** 2 - k + 1):
        for i in range(s):
            d[i] = d[i] - (c_prime[s] / s) * (nCr(s, i)) * (perf_tuple[2] ** (s - i))

    return d


def find_W(i, j, k, P, perf_tuple, sigma_list, c_list):
    sigma_prime = sigma_list[j]
    c = c_list[i]
    c_prime = c_list[j]
    d = find_d(sigma_prime, c_prime, k, P, perf_tuple)
    weight = 0
    for s in range(k ** 2 - k):
        for t in range(k ** 2 - k + 1):
            weight = weight + (c[s] * d[t]) / (s + t + 1) * (
            perf_tuple[1] ** (s + t + 1) - perf_tuple[0] ** (s + t + 1))

    return weight


if __name__ == '__main__':

    k = 4
    k_list = list(range(k))
    sigma_list = np.asarray(list(itertools.combinations_with_replacement(k_list, k)), dtype='int')
    sigma_len = len(sigma_list)
    print(sigma_len)
    P = np.array([[0.6337, 0.1753, 0.0824, 0.0494, 0.0339, 0.0253],
                  [0.1753, 0.5112, 0.1549, 0.0768, 0.0479, 0.0339],
                  [0.0824, 0.1549, 0.4865, 0.1500, 0.0768, 0.0494],
                  [0.0494, 0.0768, 0.1500, 0.4865, 0.1549, 0.0824],
                  [0.0339, 0.0479, 0.0768, 0.1549, 0.5112, 0.1753],
                  [0.0253, 0.0339, 0.0494, 0.0824, 0.1753, 0.6337]])
    alpha = 0.0
    beta = 1.0
    gamma = 0.0
    delta = 1.0
    perf_tuple = (alpha, beta, gamma, delta)

    start_time = time.time()
    prev_time = start_time
    c_list = np.zeros((sigma_len, k ** 2 - k + 1))
    for i in range(sigma_len):
        c_list[i] = find_c(sigma_list[i], k, P).T
        curr_time = time.time()
        print("i = " + str(i + 1) + " of " + str(sigma_len) + "    Time = " + str(curr_time - prev_time) + " seconds")
        prev_time = curr_time

    W = np.zeros((sigma_len, sigma_len))
    for i in range(sigma_len):
        for j in range(sigma_len):
            W[i, j] = find_W(i, j, k, P, perf_tuple, sigma_list, c_list)

    end_time = time.time()
    print("Total time = " + str(end_time - start_time) + " seconds")
    alpha = int(alpha * 10)
    beta = int(beta * 10)
    gamma = int(gamma * 10)
    delta = int(delta * 10)
    np.savetxt("weights_{}_{}_{}_{}_{}.txt".format(k, alpha, beta, gamma, delta), W, delimiter=",")
