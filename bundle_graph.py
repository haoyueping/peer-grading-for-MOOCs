#!/usr/bin/python3

from random import randint

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

    while True:
        # clear student papers
        for student in students:
            student.papers.clear()
        retry = False
        for i in range(k):
            # available paper in each round
            avai_pap = set([paper.id for paper in papers])
            for j in range(len(students)):
                # invalid paper for each student
                invalid = set(students[j].papers)
                invalid.add(students[j].id)
                # if no available paper left, retry
                if avai_pap.issubset(invalid):
                    print(avai_pap)
                    print(invalid)
                    retry = True
                    break
                while True:
                    paper = papers[randint(0, len(papers) - 1)]
                    # if the paper is invalid for the student, retry
                    if paper.id in invalid:
                        continue
                    # if the paper is choosen by others, retry
                    if paper.id not in avai_pap:
                        continue
                    avai_pap.remove(paper.id)
                    students[j].assign_paper(paper.id)
                    break
            if retry:
                break
        if retry:
            continue
        # make sure no more than one common paper between every two people
        success = True
        for i in range(n):
            for j in range(i + 1, n):
                cnt = len(students[i].papers.intersection(students[j].papers))
                if cnt >= 2:
                    print(students[i].papers)
                    print(students[j].papers)
                    success = False
                    break
            if not success:
                break
        if success:
            break

    return students

if __name__ == '__main__':
    assignments = create_bundle_graph(1000, 3)
