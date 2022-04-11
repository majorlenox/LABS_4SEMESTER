import math
import struct
import mmh3


class BloomFilter:
    FILE = 'BloomFilter.bin'
    m = 0                                   # bloom size
    n = 0                                   # text file size

    def __init__(self, m, n):
        self.m = m
        self.n = n
        self.k = int((m*8)/n * math.log(2))  # hash number
        fd = open(self.FILE, 'wb')
        fd.seek(m-1)
        fd.write('\0'.encode('ascii'))
        fd.close()

    def fill(self, textfile, sub_size):
        bloom_fd = open(self.FILE, 'ab')
        text_fd = open(textfile, 'r')
        buf = ''
        for i in range(self.n):
            if i % 1024 == 0:
                buf = text_fd.read(1024)
            s = buf[i: i+sub_size]
          #  for j in range(self.k):
            r = mmh3.hash(s, 2 * 2701) % (self.m*8)
            bloom_fd.seek(int(r/8))
            print(bytes.decode(b'\x01'))
            struct.pack('H', 1 << (r % 8))
            print(bytes(hex(1 << (r % 8)), 'ascii'))
            #print(bytes(self.tobytes(1 << (r % 8))))
            bloom_fd.write(bytes(self.tobytes(1 << (r % 8)), 'ascii'))
            text_fd.close()
            bloom_fd.close()
            return
        text_fd.close()
        bloom_fd.close()

    def tobytes(self, n):
        if len(hex(n)) == 3:
            n = '0x0' + hex(n)[3:]
            return n
        return hex(n)