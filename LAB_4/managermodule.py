from multiprocessing import Process
from bloom import *
import os

NUMBER_OF_PROCESSES = 4


def find(bloom_filter, subs_pack, textfile, first_offset):
    for sub in subs_pack:
        if bloom_filter.possibly_contains(sub):
            offset = get_offsets(sub, textfile, first_offset)
            if len(offset) != 0:
                for i in range(len(offset)):
                    print("Substring: \'" + sub + "\' was found a the offset: " + str(offset[i]))


def get_offsets(sub, textfile, first_offset):
    offsets = []
    text_fd = open(textfile, 'r')
    sub_size = len(sub)
    buf_size = sub_size * 10
    old_buf = ''
    buf = text_fd.read(buf_size)
    for i in range(os.stat(textfile).st_size - sub_size + 1):
        if i % buf_size - (buf_size - sub_size) == 0:
            old_buf = buf[buf_size - sub_size + 1: buf_size]
            s = buf[buf_size - sub_size: buf_size - 1]
            buf = text_fd.read(buf_size)
        else:
            if i % buf_size - (buf_size - sub_size) > 0:
                s = old_buf[i % (buf_size + 1) - (buf_size - sub_size + 1): sub_size - 1] + \
                    buf[0: i % (buf_size - sub_size + 1)]
            else:
                s = buf[i % buf_size: (i + sub_size) % buf_size]
        if mmh3.hash(s) == mmh3.hash(sub):
            if s == sub:  # found
                offsets.append(i)
                if first_offset:
                    return offsets
    text_fd.close()
    return offsets


def start(substrings, textfile, size_of_bloom_filter, first_offset):
    subs_fd = open(substrings, 'r')
    text_size = os.path.getsize(textfile)
    line_size = len((subs_fd.readline())) - 1
    subs_fd.close()
    bf = BloomFilter(size_of_bloom_filter, text_size - line_size + 1)
    bf.fill(textfile, line_size)
    processes = []
    subs_pack = [[] for i in range(NUMBER_OF_PROCESSES)]                # packs of lines
    n = int(os.stat(substrings).st_size / (line_size + 1))              # number of lines
    subs_fd = open(substrings, "r")
    for i in range(n):
        subs_pack[i % NUMBER_OF_PROCESSES].append(subs_fd.readline().rstrip('\n'))
    subs_fd.close()
    for j in range(NUMBER_OF_PROCESSES):
        proc = Process(target=find, args=(bf, subs_pack[j % NUMBER_OF_PROCESSES], textfile, first_offset))
        processes.append(proc)
        proc.start()
    for proc in processes:
        proc.join()
