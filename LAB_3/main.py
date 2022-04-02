import argparse
import random
import time

miller_rabin_precision = 4


def parse():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-d", help="The number for factorization is entered in decimal form", action="store_true")
    group.add_argument("-x", help="The number for factorization is entered in hexadecimal form", action="store_true")
    parser.add_argument("n", help="The number to factorize")
    args = parser.parse_args()
    if args.d | args.x == 0:
        print("Without flag -x or -d number " + args.n + " is interpreted as decimal")
    if args.x:
        return int(args.n, 16)
    return int(args.n, 10)


def extend_euclid(a, b):
    if b == 0:
        return a, 1, 0
    d, x1, y1 = extend_euclid(b, a % b)
    return d, y1, x1 - (a // b) * y1


def miller_rabin(n, s):
    for j in range(s):
        if witness(n):
            return 1  # composite number
    return 0


def witness(n):
    if n == 2:
        return False
    if n % 2 == 0:
        return True
    u = n - 1
    t = 0
    while u % 2 == 0:
        u //= 2
        t += 1
    a = random.randint(1, n - 1)
    x = modular_exponentiation(a, u, n)
    for i in range(t + 1):
        x1 = x
        x = (x ** 2) % n
        if x == 1 and x1 != 1 and x1 != n - 1:
            return True
    if x != 1:
        return True
    return False


def modular_exponentiation(a, u, n):
    c = 0
    d = 1
    b = bin(u).removeprefix('0b')
    b = list(map(int, list(b)))
    k = len(b)
    for i in range(k):
        c *= 2
        d = (d ** 2) % n
        if b[i] == 1:
            c += 1
            d = (d * a) % n
    return d


def show_factorize(n, dict):
    print(str(n) + " = ", end="")
    keys = list(dict.keys())
    keys.sort()
    for i in range(len(keys) - 1):
        if dict[keys[i]] > 1:
            print(str(keys[i]) + "^" + str(dict[keys[i]]) + " * ", end="")
        else:
            print(str(keys[i]) + " * ", end="")
    if dict[keys[len(keys) - 1]] > 1:
        print(str(keys[len(keys) - 1]) + "^" + str(dict[keys[len(keys) - 1]]))
    else:
        print(str(keys[len(keys) - 1]))


def pollard_rho(n):
    if not miller_rabin(n, miller_rabin_precision):
        return n
    d = 1
    i = 1
    y = x = random.randint(2, n - 1)
    k = 2
    while True:
        i += 1
        x = (x ** 2 - 1) % n
        if y - x == 0:
            y = x = random.randint(2, n - 1)
        else:
            d = extend_euclid(y - x, n)[0]  # can be replaced by Lehmer's GCD algorithm
        if d != 1 and d != n:
            return d
        if i == k:
            y = x
            k = 2 * k


def factorize(n):
    factors = {}
    while n != 1:
        if miller_rabin(n, miller_rabin_precision):
            d = pollard_rho(n)
            while miller_rabin(d, miller_rabin_precision):
                d = pollard_rho(d)
            if d not in factors.keys():
                r = 0
                while n % d == 0:
                    n //= d
                    r += 1
                factors[d] = r
        else:
            factors[n] = 1
            break
    return factors


if __name__ == '__main__':
    n = parse()
    t = time.time_ns()
    factors = factorize(n)
    t = time.time_ns() - t
    print('Time: %0.9f' % (float(t / 1000000000.0)) + ' seconds')
    show_factorize(n, factors)
