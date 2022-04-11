import math
import struct
import mmh3


class BloomFilter:
    FILE = 'BloomFilter.bin'
    m = 0  # bloom size
    n = 0  # text file size

    def __init__(self, m, n):
        self.m = m
        self.n = n
        self.k = int((m * 8) / n * math.log(2))  # hash number

    def fill(self, textfile, sub_size):
        bloom_fd = open(self.FILE, 'w+b')
        text_fd = open(textfile, 'r')
        buf = ''
        for i in range(self.n):
            if i % 1024 == 0:
                buf = text_fd.read(1024)
            s = buf[i: i + sub_size]
            for j in range(self.k):
                r = mmh3.hash(s, j * 2701) % (self.m * 8)
                bloom_fd.seek(int(r / 8))
                byte_before = bytes(bloom_fd.read(1))
                print(str(int(r / 8)) + " " + str((1 << (r % 8))))
                packed = bytes([int(byte_before) + int(bytes([1 << (r % 8)]), 16)])
                print(packed)
                #print(struct.pack('b', 32))
                #packed = struct.pack('@B', (1 << (r % 8)))
                #if len(byte_before) != 0:
                #    packed = struct.pack('@B', byte_before[0]|packed[0])
                bloom_fd.write(packed)
        text_fd.close()
        bloom_fd.close()
