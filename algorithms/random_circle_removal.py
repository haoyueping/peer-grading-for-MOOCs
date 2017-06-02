#!/usr/bin/python3

class Vertex:
    def __init__(self, id):
        self.id = id
        self.neighbors = set()
    def add_neighbor(self, neighbor):
        self.neighbors.add(neighbor)
    def remove_neighbor(self, neighbor):
        self.neighbors.remove(neighbor)
    def __eq__(self, other):
        return other and isinstance(other, Vertex) and other.id == self.id
    def __ne__(self, other):
        return not self.__eq__(other)
    def __hash__(self):
        return hash(self.id)
    def __str__(self):
        ids = [neighbor.id for neighbor in self.neighbors]
        return str(self.id) + ": " + str(ids)

def create_graph(rankings):
    graph = {}
    for ranking in rankings:
        create_graph_helper(ranking, graph)
    break_circles(graph)
    return graph

def create_graph_helper(ranking, graph):
    for i in range(len(ranking)):
        id = ranking[i]
        if id not in graph:
            vertex = Vertex(id)
            graph[id] = vertex
        if i != 0:
            neighbor = graph[ranking[i - 1]]
            cur = graph[id]
            cur.add_neighbor(neighbor)

def break_circles(graph):
    visiting = set()
    for id in graph:
        break_circles_helper(visiting, graph[id])

def break_circles_helper(visiting, vertex):
    # has circle
    if vertex.id in visiting:
        return True
    visiting.add(vertex.id)
    copy = set(vertex.neighbors)
    for neighbor in copy:
        if break_circles_helper(visiting, neighbor):
            vertex.remove_neighbor(neighbor)

def topological_sort(graph):
    ranking = []
    visiting = set()
    for id in graph:
        dfs(ranking, visiting, graph[id])
    return ranking;

def dfs(ranking, visiting, vertex):
    if vertex.id in visiting:
        return
    visiting.add(vertex.id)
    for neighbor in vertex.neighbors:
        dfs(ranking, visiting, neighbor)
    ranking.append(vertex.id)

def random_circle_removal(rankings):
    graph = create_graph(rankings)
    ranking = topological_sort(graph)
    return ranking
