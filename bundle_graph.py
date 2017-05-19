#!/usr/bin/python3

from random import randint

class Student:
    def __init__(self, id):
        self.id = id
        self.papers = []
    def assign_paper(self, paper):
        self.papers.append(paper)
    def __str__(self):
        return str(self.id) + ": " + str(self.papers)

class Paper:
    def __init__(self, id):
        self.id = id

def create_bundle_graph(n, k):
    students = [Student(x + 1) for x in range(n)]
    papers = [Paper(x + 1) for x in range(n)]

    while True:
        for i in range(k):
            inavai_pap = set()
            for j in range(len(students)):
                paper = None
                while True:
                    paper = papers[randint(0, len(papers) - 1)]
                    if paper.id == students[j].id:
                        continue
                    if paper.id not in inavai_pap and paper.id not in students[j].papers:
                        inavai_pap.add(paper.id)
                        break
                students[j].assign_paper(paper.id)
        # make sure not more than one paper is assigned to every two people
        success = True
        for i in range(n):
            for j in range(i + 1, n):
                cnt = len(set(students[i].papers).intersection(set(students[j].papers)))
                if cnt >= 2:
                    success = False
                    break
            if not success:
                break
        if success:
            break

    return students
