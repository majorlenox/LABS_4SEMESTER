import math
import mmh3


class BloomFilter:
    FILE = 'BloomFilter.bin'
    m = 0  # bloom size
    n = 0  # text file size
    p = 311  # prime number

    def __init__(self, m, n):
        self.m = m
        self.n = n
        self.k = int((m * 8) / n * math.log(2))  # hash number

    def fill(self, textfile, sub_size):
        text_fd = open(textfile, 'r')
        buf_size = sub_size * 10
        arr = [False] * (self.m * 8)  # array of 0 and 1
        old_buf = ''
        buf = text_fd.read(buf_size)
        for i in range(self.n):
            if i % buf_size - (buf_size - sub_size + 1) == 0:
                old_buf = buf[buf_size - sub_size + 1: buf_size - 1]
                buf = text_fd.read(buf_size)
            if i % buf_size - (buf_size - sub_size + 1) >= 0:
                s = old_buf[i % (buf_size + 1) - (buf_size - sub_size + 1): sub_size - 1] + \
                    buf[0: i % (buf_size - sub_size + 1)]
            else:
                s = buf[i: i + sub_size]
            for j in range(self.k):
                r = mmh3.hash(s, j * self.p) % (self.m * 8)
                arr[r] = True
        text_fd.close()
        bloom_fd = open(self.FILE, 'wb')
        self.binary_write(arr, bloom_fd)
        bloom_fd.close()

    @staticmethod
    def binary_write(arr, file):
        for i in range(0, len(arr), 8):
            a = arr[i] * 128 + arr[i + 1] * 64 + arr[i + 2] * 32 + + arr[i + 3] * 16 + arr[i + 4] * 8 + arr[i + 5] * 4 \
                + arr[i + 6] * 2 + arr[i + 7]
            file.write(bytes([a]))

    def possibly_contains(self, substring):
        bloom_fd = open(self.FILE, 'rb')
        for i in range(self.k):
            r = mmh3.hash(substring, i * self.p) % (self.m * 8)
            bloom_fd.seek(int(r / 8))
            cur_byte = bloom_fd.read(1)
            if int(cur_byte) & (1 << (r % 8)):
                continue
            else:
                bloom_fd.close()
                return False
        bloom_fd.close()
        return True
