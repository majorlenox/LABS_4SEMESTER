import argparse
import os
import time

import managermodule

hex_symbols = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']


def parse():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-f", help="Hash from file", default=None, type=str)
    group.add_argument('hash', help='Hash from stdin', action='store', nargs='?', type=str)
    return parser.parse_args()


class args:
    f = 'md4.txt'
    hash = '97d93003d28cabc681f37462bf73e6cd'


if __name__ == '__main__':
    # args = parse()
    if args.f is not None:
        if not os.path.exists(args.f):
            print("These file doesn't exist!")
            exit(-2)
        with open(args.f, 'r') as f_hash:
            input_md4 = f_hash.readline().removesuffix('\n')
    else:
        input_md4 = args.hash
    if len(input_md4) != 32 | (not set(input_md4).issubset(hex_symbols)):
        print("The string from file " + args.f + " is not an md4 hash!")
    t = time.time_ns()
    managermodule.work(input_md4)
    t = time.time_ns() - t
    print('Time: %0.9f' % (float(t / 1000000000.0)) + ' seconds')
