import argparse
import random

Miller_Rabin_precision = 300

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

def Miller_Rabin(n,s):
    for j in range(s):
        if Witness(n):
            return 1            # composite number
    return 0

def Witness(n):
    u = n - 1
    t = 0
    while u % 2 == 0:
        u //= 2
        t += 1
    a = random.randint(1, n - 1)
    x = Modular_Exponentiation(a, u, n)
    for i in range(t):
        x1 = x
        x = (x**2) % n
        if x == 1 and x1 != 1 and x1 != n - 1:
            return True
    if x != 1:
        return True
    return False


def Modular_Exponentiation(a, u, n):
    c = 0
    d = 1
    b = bin(u).removeprefix('0b')
    b = list(map(int, list(b)))
    k = len(b)
    for i in range(k):
        c *= 2
        d = (d**2) % n
        if b[k-i-1] == 1:
            c += 1
            d = (d*a) % n
    return d


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
    n1 = n
    i = 1
    y = x = random.randint(1, n - 1)
    k = 2
    while n != 1:
        i += 1
        x = (x ** 2 - 1) % n
        d = Extend_Euclid(abs(y - x), n)[0]  # can be replaced by Lehmer's GCD algorithm
        if d != 1 and factors.get(d) is None:
            r = 0
            while n % d == 0:
                n //= d
                r += 1
            if Miller_Rabin(d, Miller_Rabin_precision):
                dfactors = Pollard_Rho(d)
                for s in dfactors.keys():
                    factors[s] = dfactors[s] * r
            else:
                factors[d] = r
        if i == k:
            if not Miller_Rabin(n, Miller_Rabin_precision):
                factors[n] = 1
                return factors
            y = x
            k = 2 * k

    return factors


if __name__ == '__main__':
    #n = parse()
    n = 12
    factors = Pollard_Rho(n)
    Show_Factorize(n, factors)
