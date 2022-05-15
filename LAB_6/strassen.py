import numpy as np


def add_zero_lines(a):
    n, m = a.shape
    d = max(n, m)
    k = 1
    while d > 1:
        d >>= 1
        k <<= 1
    if (k == n) & (k == m):
        return a
    if (k != n) & (k != m):
        k <<= 1
    extend_m = np.zeros((n, k - m))
    extend_n = np.zeros((k - n, k))
    a = np.hstack([a, extend_m])
    a = np.vstack([a, extend_n])
    return a
