import sys


def Eulerian_cycle(graph):
    return ['a', 'b']


def Hamiltonian_cycle(graph):
    return ['a', 'b']


def get_graph_from_file(filename):
    graph = {}
    graph["A"] = ["A", "B"]
    graph["B"] = ["A", "C"]
    graph["C"] = []
    return graph


if __name__ == '__main__':

    if len(sys.argv) > 2:
        graph = get_graph_from_file(sys.argv[1])
        switcher = {
            '-E': Eulerian_cycle(graph),
            '-H': Hamiltonian_cycle(graph),
        }
        switcher.get(sys.argv[2])
    else:
        print("Not enough flags! Set name of the graph file and -H, or -E flag")
