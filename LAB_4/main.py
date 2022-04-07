import argparse
import time
import zlib
import hashlib

def parse():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-m", help="Filter Bloom size in Bytes", default=2000)
    args = parser.parse_args()
    return args

def bloom_init (m):



if __name__ == '__main__':
    args = parse()
    bloom_init(args.m)


