#!/usr/bin/python3

from datetime import datetime
from random import randint

import matplotlib.pyplot as plt


class Student:
    def __init__(self, id):
        self.id = id
        self.papers = set()

    def assign_paper(self, paper):
        self.papers.add(paper)

    def __str__(self):
        return str(self.id) + ": " + str(self.papers)

    def __eq__(self, other):
        return other and isinstance(other, Student) and other.id == self.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.id)


class Paper:
    def __init__(self, id):
        self.id = id

    def __eq__(self, other):
        return other and isinstance(other, Paper) and other.id == self.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.id)


def create_bundle_graph(n, k):
    students = [Student(x + 1) for x in range(n)]
    papers = [Paper(x + 1) for x in range(n)]

    trial = 0
    while True:
        trial = trial + 1
        # clear student papers
        for student in students:
            student.papers.clear()
        retry = False
        for i in range(k):
            # available paper in each round
            avai_pap = set([paper.id for paper in papers])
            avai_pap_list = list(avai_pap)
            for j in range(len(students)):
                # invalid paper for each student
                invalid = set(students[j].papers)
                invalid.add(students[j].id)
                # if no available paper left, retry
                if avai_pap.issubset(invalid):
                    retry = True
                    break
                while True:
                    index = randint(0, len(avai_pap_list) - 1)
                    paper = avai_pap_list[index]
                    # if the paper is invalid for the student, retry
                    if paper in invalid:
                        continue
                    # if the paper is choosen by others, retry
                    if paper not in avai_pap:
                        continue
                    avai_pap.remove(paper)
                    del avai_pap_list[index]
                    students[j].assign_paper(paper)
                    break
            if retry:
                break
        if retry:
            continue
        # make sure no more than one common paper between every two people
        success = True
        # for i in range(n):
        #     for j in range(i + 1, n):
        #         cnt = len(students[i].papers.intersection(students[j].papers))
        #         if cnt >= 2:
        #             success = False
        #             break
        #     if not success:
        #         break
        if success:
            break

    return students, trial


if __name__ == '__main__':
    plt.figure(1)
    m = 10
    n = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
    k = [6, 6, 6, 6, 6, 6, 6, 6, 6, 6]
    trial = []
    time = []
    for i in range(len(n)):
        trial.append(0)
        time.append(0)
        for j in range(m):
            start = datetime.now()
            assignments, t = create_bundle_graph(n[i], k[i])
            time[i] = time[i] + (datetime.now() - start).total_seconds()
            trial[i] = trial[i] + t
        time[i] = time[i] / m
        trial[i] = trial[i] / m
    plt.subplot(221)
    plt.plot(n, time)
    plt.ylabel('time with k fixed to 6')
    plt.show()
    plt.subplot(222)
    plt.plot(n, trial)
    plt.ylabel('number of trial with k fixed to 6')
    plt.show()

    n = [10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000]
    k = [6, 10, 14, 18, 22, 26, 30, 34, 38, 42]
    trial = []
    time = []
    for i in range(len(n)):
        trial.append(0)
        time.append(0)
        for j in range(m):
            start = datetime.now()
            assignments, t = create_bundle_graph(n[i], k[i])
            time[i] = time[i] + (datetime.now() - start).total_seconds()
            trial[i] = trial[i] + t
        time[i] = time[i] / m
        trial[i] = trial[i] / m
    plt.subplot(223)
    plt.plot(k, time)
    plt.ylabel('time with n fixed to 10000')
    plt.show()
    plt.subplot(224)
    plt.plot(k, trial)
    plt.ylabel('number of trial with n fixed to 10000')
    plt.show()
