import sys

import networkx as nx
from matplotlib import pyplot as plt


def eulerian_cycle(graph):
    G = nx.MultiDiGraph()
    t_graph = graph.copy()
    start = graph[0][0]
    cur = graph[0][0]
    path = []
    f = 1
    while f == 1:
        f = 0
        for i in range(len(t_graph)):
            if ((t_graph[i][0] == cur) & (t_graph[i][1] != start)) | \
                    ((t_graph[i][1] == cur) & (t_graph[i][0] != start)):
                if t_graph[i][0] == cur:
                    cur = t_graph[i][1]
                    G.add_edge(t_graph[i][0], t_graph[i][1])
                    path.append(t_graph[i])
                else:
                    cur = t_graph[i][0]
                    G.add_edge(t_graph[i][1], t_graph[i][0])
                    path.append([t_graph[i][1], t_graph[i][0]])
                t_graph.remove(t_graph[i])
                f = 1
                break

    while len(t_graph) > 0:
        f = 0
        for i in range(len(t_graph)):
            if (t_graph[i][0] == cur) | (t_graph[i][1] == cur):
                if t_graph[i][0] == cur:
                    cur = t_graph[i][1]
                    G.add_edge(t_graph[i][0], t_graph[i][1])
                    path.append(t_graph[i])
                else:
                    cur = t_graph[i][0]
                    G.add_edge(t_graph[i][1], t_graph[i][0])
                    path.append([t_graph[i][1], t_graph[i][0]])
                t_graph.remove(t_graph[i])
                f = 1
                break

        if f == 0:
            return -1, -1  # There is no next vertex

    if list(G.edges)[len(list(G.edges)) - 1][1] != start:
        return -1, - 1

    return G, path


def hamiltonian_cycle(graph):
    path = []
    return path


def get_graph_from_file(filepath):
    f = open(filepath, "rb")
    graph = []
    while 1:
        from_to = f.readline().split()
        if len(from_to) == 0:
            break
        graph.append([int(from_to[0]), int(from_to[1])])
    return graph


def showGraph(G, graph, flag):
    G1 = nx.MultiGraph()
    G1.add_edges_from(graph)
    pos = nx.circular_layout(G1)
    nx.draw_networkx_nodes(G, pos, node_color='r', node_size=250, alpha=1)
    nx.draw_networkx_labels(G, pos, font_size=9)
    ax = plt.gca()

    e_rad = {}

    for e in G.edges:
        e_rad[e] = e[2]

    for e in G.edges:
        e_rev = (e[1], e[0], e[2])
        if e_rad[e] == e_rad[e_rev]:
            e_rad[e] = e[2] + 1

    for e in G.edges:
        ax.annotate("",
                    xy=pos[e[0]], xycoords='data',
                    xytext=pos[e[1]], textcoords='data',
                    arrowprops=dict(arrowstyle="<-", color="0.1",
                                    shrinkA=9, shrinkB=9,
                                    patchA=None, patchB=None,
                                    connectionstyle="arc3,rad=rrr".replace('rrr', str(0.3 * e_rad[e])),
                                    ),
                    )
    ax.margins(0.05)
    plt.axis('off')
    if flag == '-E':
        plt.savefig("Eulerian_cycle", dpi=120)
    else:
        plt.savefig("Hamiltonian_cycle", dpi=120)


if __name__ == '__main__':

    sys.argv = ['main.py', '-E', 'graph.bin', '-S']

    if len(sys.argv) >= 3:
        flag = ''
        if (sys.argv.count('-E') == 1) & (sys.argv.count('-H') == 0):
            flag = '-E'
        else:
            if (sys.argv.count('-E') == 0) & (sys.argv.count('-H') == 1):
                flag = '-H'
            else:
                print("Error! You have to use flag -H or -E")
                exit(1)
        filepath = ''
        if sys.argv.count('-S') != 0:
            for i in range(3):
                if (sys.argv.index('-S') != i + 1) & (sys.argv.index(flag) != i + 1):
                    filepath = sys.argv[i + 1]
        else:
            if sys.argv.index(flag) == 1:
                filepath = sys.argv[2]
            else:
                filepath = sys.argv[1]

        graph = get_graph_from_file(filepath)
        if flag == '-E':
            G, path = eulerian_cycle(graph)
            if G == -1:
                print("There is no eulerian cycle in the graph")
                exit(0)
            k = 0
            i = path[k][0]
            print('Eulerian cycle: ')
            while k < len(path):
                print(str(i) + ' ->', end=" ")
                i = path[k][1]
                k += 1
            print(str(path[0][0]))
        else:
            path = ''

        if sys.argv.__contains__('-S'):
            showGraph(G, graph, flag)
            if flag == '-E':
                print("Eulerian cycle were saved in Eulerian_cycle.png")
            else:
                print("Hamiltonian cycle were saved in Hamiltonian_cycle.png")


    else:
        print("Not enough flags! Set name of the graph file and -H, or -E flag")
