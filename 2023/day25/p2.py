from collections import defaultdict
from copy import deepcopy
from random import choice

def contract(graph, vertex1, vertex2):
    graph[vertex1+vertex2] = [v for v in graph[vertex1]+graph[vertex2] if v not in (vertex1, vertex2)]
    # remove connections to old vertices
    for vertex in graph[vertex1+vertex2]:
        if vertex not in (vertex1, vertex2):
            # filter out connections to old vertices
            graph[vertex] = [v for v in graph[vertex] if v not in (vertex1, vertex2)]
            # add the new vertex
            graph[vertex].append(vertex1+vertex2)
    del graph[vertex1]
    del graph[vertex2]

def kargers_algorithm(graph):
    while len(graph) > 2:
        random_vertex = choice(list(graph.keys()))
        vertex_choices = random_vertex, choice(graph[random_vertex])
        contract(graph, vertex_choices[0], vertex_choices[1])
    return graph

with open("input.txt") as file:
    graph = defaultdict(list)
    for line in file:
        left, right = line.strip().split(": ")
        right = right.split(" ")
        for vertex in right:
            graph[left].append(vertex)
            graph[vertex].append(left)

    for i in range(100):
        graph_copy = deepcopy(graph)
        kargers_algorithm(graph_copy)
        product = 1
        for k,v in graph_copy.items():
            product *= len(k)//3
            cut_size = len(v)
        if cut_size == 3:
            print(product)
            break