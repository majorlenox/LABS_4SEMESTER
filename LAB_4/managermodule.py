import os
from multiprocessing import Process
from bloom import *

NUMBER_OF_PROCESSES = 4

def find

def get_offset

def start(substrings, textfile, size_of_bloom_filter):
    f_subs = open(substrings, 'r')
    text_size = os.path.getsize(substrings)
    line_size = len((f_subs.readline()))
    f_subs.close()
    bf = BloomFilter(size_of_bloom_filter, text_size - line_size + 1)
    bf.fill(textfile, line_size)
    processes = [] * NUMBER_OF_PROCESSES
    with open(substrings, "r") as f_subs:
        while True:
            # Add processing of substrings packs