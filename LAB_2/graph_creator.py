import networkx as nx
import matplotlib.pyplot as plt

import random
import sys


# Visualisation


def showGraph(graph):
    G = nx.MultiGraph()
    G.add_edges_from(graph)
    pos = nx.circular_layout(G)
    nx.draw_networkx_nodes(G, pos, node_color='r', node_size=250, alpha=1)
    nx.draw_networkx_labels(G, pos, font_size=9)
    ax = plt.gca()
    for e in G.edges:
        ax.annotate("",
                    xy=pos[e[0]], xycoords='data',
                    xytext=pos[e[1]], textcoords='data',
                    arrowprops=dict(arrowstyle="-", color="0.1",
                                    shrinkA=9, shrinkB=9,
                                    patchA=None, patchB=None,
                                    connectionstyle="arc3,rad=rrr".replace('rrr', str(0.3 * e[2])),
                                    ),
                    )
    ax.margins(0.05)
    plt.axis('off')
    plt.savefig("graph", dpi=120)


# Generation

def kruskals_algorithm(graph, E, vertexes):
    V = len(vertexes)
    E -= V - 1
    color = {}
    for i in range(V):
        color[vertexes[i]] = vertexes[i]

    while len(set(list(color.values()))) != 1:
        v_from = vertexes[random.randint(0, V - 1)]
        v_to = vertexes[random.randint(0, V - 1)]
        if color[v_from] != color[v_to]:
            temp_color = color[v_to]
            for i in range(V):
                if color[vertexes[i]] == temp_color:
                    color[vertexes[i]] = color[v_from]
            graph.append([v_from, v_to])


def saveGraph(graph):
    f = open('graph.bin', 'wb')
    for e in graph:
        bt = bytes(str(e[0]) + ' ' + str(e[1]) + '\n', encoding='utf-8')
        f.write(bt)
    f.close()


if __name__ == '__main__':

    # init V,E
    V = 5
    if sys.argv.__contains__('-V'):
        V = int(sys.argv[sys.argv.index('-V') + 1])
    E = random.randint(V - 1, V * 2)

    if sys.argv.__contains__('-E'):
        E = int(sys.argv[sys.argv.index('-E') + 1])
        if (E < V - 1) | (V <= 0):
            print("It is impossible to create a connected graph")
            exit(1)
    #

    graph = []  # list of edges
    vertexes = []

    # naming
    name_from = 100
    name_to = name_from * 10 - 1
    while V >= (name_from * 10 - name_from):
        name_from *= 10
        name_to = name_from * 10 - 1

    for v in range(V):
        r = random.randint(name_from, name_to)
        while r in vertexes:
            r = random.randint(name_from, name_to)
        vertexes.append(r)

    kruskals_algorithm(graph, E, vertexes)  # only linked graphs

    for e in range(E - (V - 1)):
        v_from = vertexes[random.randint(0, V - 1)]
        v_to = vertexes[random.randint(0, V - 1)]
        while v_to == v_from:  # no zero cycles
            v_to = vertexes[random.randint(0, V - 1)]
        graph.append([v_from, v_to])
    if sys.argv.__contains__("-S"):
        showGraph(graph)
        print("The graph image was saved in a file graph.png")
    saveGraph(graph)
    print("The graph was saved in graph.bin")
