import argparse
import math
import mmh3
import time
import zlib
import hashlib
from bloom import *
import os


def parse():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-m", help="Filter Bloom size in Bytes", default=2000)
    parser.add_argument('substrings', help='path to file with substrings', action='store', type=str)
    parser.add_argument('text', help='path to file with text', action='store', type=str)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse()
    if (not os.path.exists(args.substrings)) | (not os.path.exists(args.text)):
        print("These files don't exist!")
        exit(-2)

    f_subs = open(args.substrings, 'r')

    text_size = os.path.getsize(str(args.text))
    line_size = len((f_subs.readline()))

    a = bloom_filter(m, )
    bloom_init(args.m, text_size - line_size + 1)
