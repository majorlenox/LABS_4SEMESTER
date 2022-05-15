import numpy as np

RAND_DIGITS = 2
RAND_RANGE = 100


def multiply_and_round(a):
    return round(a * RAND_RANGE, RAND_DIGITS)


def generate_matrices(n, mn, m):
    matrix_a = np.zeros((n, mn))
    matrix_b = np.zeros((mn, m))
    for i in range(n):
        matrix_a[i, :] = list(map(multiply_and_round, np.random.rand(mn)))
    for i in range(mn):
        matrix_b[i, :] = list(map(multiply_and_round, np.random.rand(m)))
    return matrix_a, matrix_b


def load_matrices(filename):
    with open(filename, 'r') as f_matrices:
        f_matrices.readline()
        line = f_matrices.readline().split(" ")
        row = []
        for element in line:
            row.append(float(element))
        matrix_a = np.array(row)
        line = f_matrices.readline().split(" ")
        while line[0] != "Matrix":
            row = []
            for element in line:
                row.append(float(element))
            matrix_a = np.vstack([matrix_a, np.array(row)])
            line = f_matrices.readline().split(" ")
            if line == ['']:
                print("Incorrect matrices file: " + filename + "!")
                return None, None
        line = f_matrices.readline().split(" ")
        row = []
        for element in line:
            row.append(float(element))
        matrix_b = np.array(row)
        line = f_matrices.readline().split(" ")
        while line != [""]:
            row = []
            for element in line:
                row.append(float(element))
            matrix_b = np.vstack([matrix_b, np.array(row)])
            line = f_matrices.readline().split(" ")
    return matrix_a, matrix_b


def show_matrix(matrix):
    print(matrix)


def multiply_matrices(matrix_a, matrix_b):
    n, mn1 = matrix_a.shape
    mn2, m = matrix_b.shape
    if mn1 != mn2:
        print("Can't multiply matrices with incorrect sizes!")
        return -1
    matrix_c = np.zeros((n, m))
    for i in range(n):
        for j in range(m):
            for k in range(mn1):
                matrix_c[i, j] += matrix_a[i, k] * matrix_b[k, j]
    return matrix_c


def compare_three_matrices(mx1, mx2, mx3):
    return (mx1 == mx2).all() & (mx2 == mx3).all()


def save_result_matrix(matrix_c, filename):
    with open(filename, 'w') as f_matrices:
        f_matrices.write("Matrix C:\n")
        for row in matrix_c:
            f_matrices.write(' '.join([str(a) for a in row]) + '\n')


def save_matrices(matrix_a, matrix_b, filename):
    with open(filename, 'w') as f_matrices:
        f_matrices.write("Matrix A:\n")
        for row in matrix_a:
            f_matrices.write(' '.join([str(a) for a in row]) + '\n')
        f_matrices.write("Matrix B:\n")
        for row in matrix_b:
            f_matrices.write(' '.join([str(a) for a in row]) + '\n')
