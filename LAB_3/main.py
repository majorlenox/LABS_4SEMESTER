import argparse
import math
import random


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


def Extend_Euclid(a, b):
    if b == 0:
        return a, 1, 0
    d, x1, y1 = Extend_Euclid(b, a % b)
    return d, y1, x1 - (a // b) * y1


def Show_Factorize(n, dict):
    print(str(n) + " = ", end="")
    keys = list(dict.keys())
    for i in range(len(keys) - 1):
        if dict[keys[i]] > 1:
            print(str(keys[i]) + "^" + str(dict[keys[i]]) + " * ", end="")
        else:
            print(str(keys[i]) + " * ", end="")
    if dict[keys[len(keys) - 1]] > 1:
        print(str(keys[len(keys) - 1]) + "^" + str(dict[keys[len(keys) - 1]]))
    else:
        print(str(keys[len(keys) - 1]))


def Pollard_Rho(n):
    factors = {}  # prime divisors
    visited = {}
    n1 = n
    i = 1
    y = x = random.randint(0, n - 1)
    k = 2
    while n != 1:
        i += 1
        x = (x ** 2 - 1) % n
        d = Extend_Euclid(y - x, n)[0]  # can be replaced by Lehmer's GCD algorithm
        if visited.get(x) is not None:
            if factors.get(n) and n != 1:
                factors[n] += 1
            else:
                factors[n] = 1
            break
        visited[x] = 1
        if d != 1 and d != n1 and factors.get(d) is None:
            dfactors = Pollard_Rho(d)
            r = 0
            while n % d == 0:
                n = n // d
                r += 1
            for s in dfactors.keys():
                factors[s] = dfactors[s] * r
        if i == k:
            y = x
            k = 2 * k
    return factors


if __name__ == '__main__':
    #    n = parse()
    n = 123
    factors = Pollard_Rho(n)
    Show_Factorize(n, factors)
