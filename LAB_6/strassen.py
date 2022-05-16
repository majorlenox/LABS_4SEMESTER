import numpy as np


def divide_matrix(A):
    n, m = A.shape
    return A.reshape(2, m // 2, -1, m // 2).swapaxes(1, 2).reshape(-1, m // 2, m // 2)


def add_zero_lines(A):
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


def remove_zero_lines(A, n, m):
    return A[:n, :m]


def multiply(A, B):
    C = np.zeros(A.shape)
    if A.shape[0] == 1:
        C[0, 0] = A[0, 0] * B[0, 0]
        return C

    k = A.shape[0] // 2

    A_11, A_12, A_21, A_22 = A[:k, :k], A[:k, k:], A[k:, :k], A[k:, k:]
    B_11, B_12, B_21, B_22 = B[:k, :k], B[:k, k:], B[k:, :k], B[k:, k:]

    D = multiply(A_11 + A_22, B_11 + B_22)
    D_1 = multiply(A_12 - A_22, B_21 + B_22)
    D_2 = multiply(A_21 - A_11, B_11 + B_12)
    H_1 = multiply(A_11 + A_12, B_22)
    H_2 = multiply(A_21 + A_22, B_11)
    V_1 = multiply(A_22, B_21 - B_11)
    V_2 = multiply(A_11, B_12 - B_22)

    C[:k, :k] = D + D_1 + V_1 - H_1
    C[:k, k:] = V_2 + H_1
    C[k:, :k] = V_1 + H_2
    C[k:, k:] = D + D_2 + V_2 - H_2

    return C


def work(A, B):
    prev_A = A.shape
    prev_B = B.shape
    A = add_zero_lines(A)
    B = add_zero_lines(B)
    C = multiply(A, B)
    C = remove_zero_lines(C, prev_A[0], prev_B[1])
    return C
