import random
import sys

def check_cycle(graph):
    E = 0
    for v in range(V):
        while (graph[v+1].has(v+1)):

            E += 1
    return E

if __name__ == '__main__':

    # init V,E
    V = 100
    E = random.randint(int(V - 1), V * 3)

    if len(sys.argv) == 1:
        V = int(sys.argv[1])
        E = random.randint(int(V - 1), V * 3)

    if len(sys.argv) == 2:
        V = int(sys.argv[1])
        E = int(sys.argv[2])
        if E < V - 1:
            print("It is impossible to create a connected graph")
            exit(1)
    #

    graph = {}

    for v in range(V):
        graph[v+1] = []

    for e in range(E):
        graph[random.randint(1, V)].append(random.randint(1, V))

    while (cycles = check_cycle(graph)):

