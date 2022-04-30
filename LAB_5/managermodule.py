import struct
from multiprocessing import Process

from md4 import MD4

NUMBER_OF_PROCESSES = 1


def inner_loop(s, input_md4):
    input_md4 = [input_md4[i: i + 4] for i in range(4)]
    input_md4[0] = (int(input_md4[0], 16) - 0x67452301) & MD4.mask
    input_md4[1] = (int(input_md4[1], 16) - 0xEFCDAB89) & MD4.mask
    input_md4[2] = (int(input_md4[2], 16) - 0x98BADCFE) & MD4.mask
    input_md4[3] = (int(input_md4[3], 16) - 0x10325476) & MD4.mask
    # s = x1
    s_len = MD4.get_length(s)
    s += b'\x80'
    s += b'\x00' * (52 - len(s))
    s += struct.pack("<L", s_len) + b'\x00' * 4  # s = x1 + '100000' + len + '4 bytes of 0', len(s) = 120
    s1 = b'\x00\x00\x00\x00' + s
    x = list(struct.unpack("<16I", s1))
    x1 = [0] * 16
    x2 = [0] * 16
    for i in range(16):
        x1[i] = (x[i] + 0x5A827999) & MD4.mask
        x2[i] = (x[i] + 0x6ED9EBA1) & MD4.mask
    expected = MD4.reverse(input_md4, x1, x2)

    for x0 in range(0xFFFFFFFF + 1):
        s1 = struct.pack("<L", x0) + s
        x = list(struct.unpack("<16I", s1))
        x[0] = x0
        x1[0] = (x1[0] + 1) & MD4.mask
        x2[0] = (x2[0] + 1) & MD4.mask
        if MD4.hash_optimized_compare(input_md4, x, x1, x2, expected):
            print("preimage founded: " + s1[0:s_len].hex())


def inner_loop_0(input_md4):  # x1 = 00000000 (length changeable)
    input_md4 = [input_md4[i: i + 4] for i in range(4)]
    input_md4[0] = (int(input_md4[0], 16) - 0x67452301) & MD4.mask
    input_md4[1] = (int(input_md4[1], 16) - 0xEFCDAB89) & MD4.mask
    input_md4[2] = (int(input_md4[2], 16) - 0x98BADCFE) & MD4.mask
    input_md4[3] = (int(input_md4[3], 16) - 0x10325476) & MD4.mask
    x = [0] * 16
    x1 = [0x5A827999] * 16
    x2 = [0x6ED9EBA1] * 16
    x[0] = 128
    x1[0] += 128
    x2[0] += 128
    if MD4.hash_compare(input_md4, x, x1, x2):
        print("preimage founded: " + hex(x[0]))
    for c in range(1, 0xFFFFFFFF + 1, 1):
        if c < 0xFF:
            r = 8
            x[0] = 0x100 * 128
            x1[0] = (0x100 * 128 + 0x5A827999) & MD4.mask
            x2[0] = (0x100 * 128 + 0x6ED9EBA1) & MD4.mask
        else:
            if c < 0xFFFF:
                r = 16
                x[0] = 0x10000 * 128
                x1[0] = (0x10000 * 128 + 0x5A827999) & MD4.mask
                x2[0] = (0x10000 * 128 + 0x6ED9EBA1) & MD4.mask
            else:
                if c < 0xFFFFFF:
                    r = 24
                    x[0] = 0x1000000 * 128
                    x1[0] = (0x1000000 * 128 + 0x5A827999) & MD4.mask
                    x2[0] = (0x1000000 * 128 + 0x6ED9EBA1) & MD4.mask
                else:
                    r = 32
                    x[1] = 128
                    x1[1] = 0x5A827999 + 128
                    x2[1] = 0x6ED9EBA1 + 128
        x[0] += c
        x1[0] += c
        x2[0] += c
        x[14] = r
        x1[14] = 0x5A827999 + r
        x2[14] = 0x6ED9EBA1 + r
        if MD4.hash_compare(input_md4, x, x1, x2):
            print("preimage founded: " + hex(x[0]))


def work(input_md4):
    processes = [Process()] * NUMBER_OF_PROCESSES
    # outer loop
    proc = Process(target=inner_loop_0, args=[input_md4])
    processes[0] = proc
    proc.start()
    for x1 in range(1, 0xFFFFFFFF + 1):
        x1b = struct.pack("<L", x1)
        proc = Process(target=inner_loop, args=(x1b, input_md4))
        processes[x1 % NUMBER_OF_PROCESSES] = proc
        proc.start()
        if x1 % NUMBER_OF_PROCESSES == NUMBER_OF_PROCESSES - 1:
            for proc in processes:
                proc.join()
