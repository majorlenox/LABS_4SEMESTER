import numpy as np

RAND_DIGITS = 2
RAND_RANGE = 100


def generate_matrices(n, mn, m):
    matrix_a = [[0 for i in range(mn)] for j in range(n)]
    matrix_b = [[0 for i in range(m)] for j in range(mn)]
    for i in range(n):
        for j in range(mn):
            matrix_a[i][j] = round(np.random.rand() * RAND_RANGE, RAND_DIGITS)
            for k in range(m):
                matrix_b[j][k] = round(np.random.rand() * RAND_RANGE, RAND_DIGITS)
    return matrix_a, matrix_b


def load_matrices(filename):
    matrix_a = []
    matrix_b = []
    with open(filename, 'r') as f_matrices:
        f_matrices.readline()
        line = f_matrices.readline().split(" ")
        while line[0] != "Matrix":
            matrix_a.append([])
            for element in line:
                matrix_a[len(matrix_a) - 1].append(float(element))
            line = f_matrices.readline().split(" ")
            if line == ['']:
                print("Incorrect matrices file: " + filename + "!")
                return -1, -1
        line = f_matrices.readline().split(" ")
        while line != [""]:
            matrix_b.append([])
            for element in line:
                matrix_b[len(matrix_b) - 1].append(float(element))
            line = f_matrices.readline().split(" ")
    return matrix_a, matrix_b


def show_matrix(matrix):
    print(np.matrix(matrix))


def save_matrices(matrix_a, matrix_b, filename):
    with open(filename, 'w') as f_matrices:
        f_matrices.write("Matrix A:\n")
        for row in matrix_a:
            f_matrices.write(' '.join([str(a) for a in row]) + '\n')
        f_matrices.write("Matrix B:\n")
        for row in matrix_b:
            f_matrices.write(' '.join([str(a) for a in row]) + '\n')
