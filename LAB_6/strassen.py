from multiprocessing import Pool

import numpy as np

TRIVIAL_MULTIPLICATION_BOUND = 32


# np.array realization BEGIN

def add_zero_lines_np(A):
    n, m = A.shape
    d = max(n, m)
    k = 1
    while d > 1:
        d >>= 1
        k <<= 1
    if (k == n) & (k == m):
        return A
    if (k != n) & (k != m):
        k <<= 1
    extend_m = np.zeros((n, k - m))
    extend_n = np.zeros((k - n, k))
    A = np.hstack([A, extend_m])
    A = np.vstack([A, extend_n])
    return A


def remove_zero_lines_np(A, n, m):
    return A[:n, :m]


def multiply_np(A, B):
    n = A.shape[0]
    C = np.zeros((n, n))
    if n == 1:
        C[0, 0] = A[0, 0] * B[0, 0]
        return C
    if n < TRIVIAL_MULTIPLICATION_BOUND:
        A = A.tolist()
        B = B.tolist()
        C = [[0] * n for i in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return np.matrix(C)

    k = n // 2

    A_11, A_12, A_21, A_22 = A[:k, :k], A[:k, k:], A[k:, :k], A[k:, k:]
    B_11, B_12, B_21, B_22 = B[:k, :k], B[:k, k:], B[k:, :k], B[k:, k:]

    D = multiply_np(A_11 + A_22, B_11 + B_22)
    D_1 = multiply_np(A_12 - A_22, B_21 + B_22)
    D_2 = multiply_np(A_21 - A_11, B_11 + B_12)
    H_1 = multiply_np(A_11 + A_12, B_22)
    H_2 = multiply_np(A_21 + A_22, B_11)
    V_1 = multiply_np(A_22, B_21 - B_11)
    V_2 = multiply_np(A_11, B_12 - B_22)

    C[:k, :k] = D + D_1 + V_1 - H_1
    C[:k, k:] = V_2 + H_1
    C[k:, :k] = V_1 + H_2
    C[k:, k:] = D + D_2 + V_2 - H_2

    return C

# np array realization END

# list realization


def divide_matrix(A):
    n = len(A)
    k = n // 2
    A_11 = [[A[i][j] for j in range(0, k)] for i in range(0, k)]
    A_12 = [[A[i][j] for j in range(k, n)] for i in range(0, k)]
    A_21 = [[A[i][j] for j in range(0, k)] for i in range(k, n)]
    A_22 = [[A[i][j] for j in range(k, n)] for i in range(k, n)]
    return A_11, A_12, A_21, A_22


def add_zero_lines(A):
    n, m = len(A), len(A[0])
    d = max(n, m)
    k = 1
    while d > 1:
        d >>= 1
        k <<= 1
    if (k == n) & (k == m):
        return A
    if (k != n) & (k != m):
        k <<= 1
    B = [[A[i][j] if (i < n) & (j < m) else 0 for j in range(k)] for i in range(k)]
    return B


def remove_zero_lines(A, n, m):
    return [[A[i][j] for j in range(m)] for i in range(n)]


def add(A, B):
    n = len(A)
    return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]


def sub(A, B):
    n = len(A)
    return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]


def calculate_c(D, D_1, D_2, H_1, H_2, V_1, V_2):
    n = len(D) * 2
    k = len(D)
    C = [[0] * n for i in range(n)]
    for i in range(k):
        for j in range(k):
            C[i][j] = D[i][j] + D_1[i][j] + V_1[i][j] - H_1[i][j]
    for i in range(k):
        for j in range(k):
            C[i][j + k] = V_2[i][j] + H_1[i][j]
    for i in range(k):
        for j in range(k):
            C[i + k][j] = V_1[i][j] + H_2[i][j]
    for i in range(k):
        for j in range(k):
            C[i + k][j + k] = D[i][j] + D_2[i][j] + V_2[i][j] - H_2[i][j]
    return C


def multiply(A, B):
    n = len(A)
    if n == 1:
        return [[A[0][0] * B[0][0]]]

    if n < TRIVIAL_MULTIPLICATION_BOUND:
        C = [[0] * n for i in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    A_11, A_12, A_21, A_22 = divide_matrix(A)
    B_11, B_12, B_21, B_22 = divide_matrix(B)

    D = multiply(add(A_11, A_22), add(B_11, B_22))
    D_1 = multiply(sub(A_12, A_22), add(B_21, B_22))
    D_2 = multiply(sub(A_21, A_11), add(B_11, B_12))
    H_1 = multiply(add(A_11, A_12), B_22)
    H_2 = multiply(add(A_21, A_22), B_11)
    V_1 = multiply(A_22, sub(B_21, B_11))
    V_2 = multiply(A_11, sub(B_12, B_22))

    C = calculate_c(D, D_1, D_2, H_1, H_2, V_1, V_2)

    return C


#

def multiply_multiprocess_np(A, B):
    n = A.shape[0]
    C = np.zeros((n, n))
    if n == 1:
        C[0, 0] = A[0, 0] * B[0, 0]
        return C
    if n < TRIVIAL_MULTIPLICATION_BOUND:
        A = A.tolist()
        B = B.tolist()
        C = [[0] * n for i in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return np.matrix(C)

    k = n // 2

    A_11, A_12, A_21, A_22 = A[:k, :k], A[:k, k:], A[k:, :k], A[k:, k:]
    B_11, B_12, B_21, B_22 = B[:k, :k], B[:k, k:], B[k:, :k], B[k:, k:]

    tasks = ((A_11 + A_22, B_11 + B_22), (A_12 - A_22, B_21 + B_22), (A_21 - A_11, B_11 + B_12), (A_11 + A_12, B_22),
             (A_21 + A_22, B_11), (A_22, B_21 - B_11), (A_11, B_12 - B_22))

    pool = Pool(processes=7)
    p = pool.starmap(multiply_np, [k for k in tasks])
    pool.close()

    C[:k, :k] = p[0] + p[1] + p[5] - p[3]
    C[:k, k:] = p[6] + p[3]
    C[k:, :k] = p[5] + p[4]
    C[k:, k:] = p[0] + p[2] + p[6] - p[4]

    return C


def work(A, B, m):
    if m == 1:      # list implementation, one process
        A = A.tolist()
        B = B.tolist()
        prev_A = len(A)
        prev_B = len(B[0])
        A = add_zero_lines(A)
        B = add_zero_lines(B)
        C = multiply(A, B)
        C = remove_zero_lines(C, prev_A, prev_B)
        C = np.matrix(C)
        return C
    prev_A = A.shape
    prev_B = B.shape
    A = add_zero_lines_np(A)
    B = add_zero_lines_np(B)
    if m == 2:
        C = multiply_np(A, B)
    else:
        C = multiply_multiprocess_np(A, B)
    C = remove_zero_lines_np(C, prev_A[0], prev_B[1])
    return C


