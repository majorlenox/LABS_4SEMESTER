import networkx as nx
import matplotlib.pyplot as plt

import random
import sys


# Visualisation

def showGraph(graph, vertexes):
    G = nx.Graph()
    G.add_edges_from(graph)
    color_map = ["red" for i in range(len(vertexes))]
    nx.draw_networkx(G, with_labels=True, font_color='black', font_size=16, node_color=color_map)
    plt.savefig("Graph", dpi=120)


# Generation

def kruskals_algorithm(graph, E, vertexes):
    V = len(vertexes)
    E -= V - 1
    color = {}
    for i in range(V):
        color[vertexes[i]] = vertexes[i]

    for e in range(V - 1):
        while len(set(list(color.values()))) != 1:
            v_from = vertexes[random.randint(0, V - 1)]
            v_to = vertexes[random.randint(0, V - 1)]
            if color[v_from] != color[v_to]:
                for i in range(V - 1):
                    if color[vertexes[i]] == color[v_to]:
                        color[vertexes[i]] = color[v_from]
                graph.append([v_from, v_to])


if __name__ == '__main__':

    # init V,E
    V = 10
    if sys.argv.__contains__('-V'):
        V = int(sys.argv[sys.argv.index('-V') + 1])
    E = random.randint(V - 1, V * 2)

    if sys.argv.__contains__('-E'):
        E = int(sys.argv[sys.argv.index('-E') + 1])
        if (E < V - 1) | (V <= 0):
            print("It is impossible to create a connected graph")
            exit(1)
    #

    graph = []
    vertexes = []

    # naming
    name_from = 100
    name_to = name_from * 10 - 1
    while V >= (name_from * 10 - name_from):
        name_from *= 10
        name_to = name_from * 10 - 1

    for v in range(V):
        vertexes.append(random.randint(name_from, name_to))

    kruskals_algorithm(graph, E, vertexes)  # only linked graphs

    for e in range(E - (V - 1)):
        v_from = vertexes[random.randint(0, V - 1)]
        v_to = vertexes[random.randint(0, V - 1)]
        while v_to == v_from:  # no zero cycles
            v_to = vertexes[random.randint(0, V - 1)]
        graph.append([v_from, v_to])
    if sys.argv.__contains__("-S"):
        showGraph(graph, vertexes)
