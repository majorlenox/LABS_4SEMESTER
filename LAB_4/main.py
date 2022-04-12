import argparse
import os

import managermodule


def parse():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-m", help="Filter Bloom size in Bytes", default=2000, type=int)
    parser.add_argument('substrings', help='path to file with substrings', action='store', type=str)
    parser.add_argument('text', help='path to file with text', action='store', type=str)
    args = parser.parse_args()
    return args


# class args:
#    m = 10
#    substrings = 'substrings.txt'
#    text = 'text.txt'

if __name__ == '__main__':
    args = parse()
    if (not os.path.exists(args.substrings)) | (not os.path.exists(args.text)):
        print("These files don't exist!")
        exit(-2)
    managermodule.start(args.substrings, args.text, args.m)
