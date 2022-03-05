import sys


def eulerian_cycle(graph):
    path = []
    return path



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


if __name__ == '__main__':

    if len(sys.argv) == 3:
        flag = ''
        if (sys.argv.count('-E') == 1) & (sys.argv.count('-H') == 0):
            flag = '-E'
        else:
            if (sys.argv.count('-E') == 0) & (sys.argv.count('-H') == 1):
                flag = '-H'
            else:
                print("Error! You have to use flag -H or -E")
                exit(1)
        if sys.argv.index(flag) == 1:
            filepath = sys.argv[2]
        else:
            filepath = sys.argv[1]
        graph = get_graph_from_file(filepath)
        if flag == '-E':
            path = eulerian_cycle(graph)

    else:
        print("Not enough flags! Set name of the graph file and -H, or -E flag")
