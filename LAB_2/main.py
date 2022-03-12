import sys

import networkx as nx
from matplotlib import pyplot as plt


def is_eulerian_graph(graph):
    degree = {}
    for e in graph:
        degree[e[0]] = 0
        degree[e[1]] = 0

    for e in graph:
        degree[e[0]] += 1
        degree[e[1]] += 1

    for v in degree:
        if degree[v] % 2 != 0:
            return False
    return True


def eulerian_cycle(graph):
    if not is_eulerian_graph(graph):
        return -1, -1
    G = nx.MultiDiGraph()
    t_graph = graph.copy()
    start = graph[0][0]
    curr = graph[0][0]
    path = []
    f = 1
    while f == 1:
        f = 0
        for i in range(len(t_graph)):
            if ((t_graph[i][0] == curr) & (t_graph[i][1] != start)) | \
                    ((t_graph[i][1] == curr) & (t_graph[i][0] != start)):
                if t_graph[i][0] == curr:
                    curr = t_graph[i][1]
                    G.add_edge(t_graph[i][0], t_graph[i][1])
                    path.append(t_graph[i])
                else:
                    curr = t_graph[i][0]
                    G.add_edge(t_graph[i][1], t_graph[i][0])
                    path.append([t_graph[i][1], t_graph[i][0]])
                t_graph.remove(t_graph[i])
                f = 1
                break
        if f == 0:
            for i in range(len(t_graph)):
                if (t_graph[i][0] == curr) | (t_graph[i][1] == curr):
                    if t_graph[i][0] == curr:
                        curr = t_graph[i][1]
                        G.add_edge(t_graph[i][0], t_graph[i][1])
                        path.append(t_graph[i])
                    else:
                        curr = t_graph[i][0]
                        G.add_edge(t_graph[i][1], t_graph[i][0])
                        path.append([t_graph[i][1], t_graph[i][0]])
                    t_graph.remove(t_graph[i])
                    f = 1
                    break
            if f == 0:
                break        # There is no next vertex

    if path[len(path) - 1][1] != start:
        return -1, - 1

    return G, path


def hamiltonian_cycle(g):
    graph = g.copy()
    graph = to_adjacency_list(graph)
    N = len(graph.keys())
    curr = g[0][0]
    path = [curr]
    path = hamilton(graph, curr, path, N)
    return path


def hamilton(graph, curr, path, N):
    for v in graph.get(curr):
        if (len(path) == N) & (v == path[0]):
            path.append(v)
            return path
        if not (v in path):
            path.append(v)
            if len(hamilton(graph, v, path, N)) == N + 1:
                return path
            path.pop()
    return []


def to_adjacency_list(graph):
    adj = {}
    for e in graph:
        adj[e[0]] = set()
        adj[e[1]] = set()
    for e in graph:
        adj[e[0]].add(e[1])
        adj[e[1]].add(e[0])
    return adj


def get_graph_from_file(filepath):
    f = open(filepath, "rb")
    graph = []
    while 1:
        from_to = f.readline().split()
        if len(from_to) == 0:
            break
        graph.append([int(from_to[0]), int(from_to[1])])
    return graph


def showGraph_eulerian(G, graph):
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
        if e_rad.get(e_rev) is not None:
            if e_rad[e] == e_rad[e_rev]:
                e_rad[e] = e[2] + 1
                k = e[2] + 1
                while e_rad.get((e[0], e[1], k)) is not None:
                    e_rad[(e[0], e[1], k)] += 1
                    k += 1
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
    plt.savefig("Eulerian_cycle", dpi=120)


def showGraph_hamiltonian(path, graph):
    G = nx.MultiGraph()
    G.add_edges_from(graph)
    pos = nx.circular_layout(G)
    nx.draw_networkx_nodes(G, pos, node_color='r', node_size=250, alpha=1)
    nx.draw_networkx_labels(G, pos, font_size=9)
    ax = plt.gca()
    arr = {}
    edge_color = {}

    for i in range(len(path) - 1):
        arr[(path[i], path[i + 1], 0)] = 1
        arr[(path[i + 1], path[i], 0)] = -1
        edge_color[(path[i], path[i + 1], 0)] = 'b'
        edge_color[(path[i + 1], path[i], 0)] = 'b'

    for e in G.edges:
        if arr.get(e) == 1:
            arrowstyle = '<-'
        else:
            if arr.get(e) == -1:
                arrowstyle = '->'
            else:
                arrowstyle = '-'
                edge_color[e] = '0.1'
        ax.annotate("",
                    xy=pos[e[0]], xycoords='data',
                    xytext=pos[e[1]], textcoords='data',
                    arrowprops=dict(arrowstyle=arrowstyle, color=edge_color[e],
                                    shrinkA=9, shrinkB=9,
                                    patchA=None, patchB=None,
                                    connectionstyle="arc3,rad=rrr".replace('rrr', str(0.3 * e[2])),
                                    ),
                    )
    ax.margins(0.05)
    plt.axis('off')
    plt.savefig("Hamiltonian_cycle", dpi=120)


if __name__ == '__main__':
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
            path = hamiltonian_cycle(graph)
            if len(path) == 0:
                print("There is no hamiltonian cycle in the graph")
                exit(0)
            print('Hamiltonian cycle: ')
            for i in range(len(path) - 1):
                print(str(path[i]) + ' ->', end=" ")
            print(str(path[len(path) - 1]))

        if '-S' in sys.argv:
            if flag == '-E':
                showGraph_eulerian(G, graph)
                print("Eulerian cycle were saved in Eulerian_cycle.png")
            else:
                showGraph_hamiltonian(path, graph)
                print("Hamiltonian cycle were saved in Hamiltonian_cycle.png")
    else:
        print("Not enough flags! Set name of the graph file and -H, or -E flag")
