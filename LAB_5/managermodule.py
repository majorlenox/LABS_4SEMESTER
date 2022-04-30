import struct
from multiprocessing import Process

from md4 import MD4

NUMBER_OF_PROCESSES = 1


def inner_loop(s, input_md4):
    input_md4 = [input_md4[i: i + 8] for i in range(0, 32, 8)]
    for i in range(4):
        input_md4[i] = [input_md4[i][0:2], input_md4[i][2:4], input_md4[i][4:6], input_md4[i][6:8]]
    for j in range(4):
        input_md4[j] = int(input_md4[j][3], 16) * 0x1000000 + int(input_md4[j][2], 16) * 0x10000 + \
                       int(input_md4[j][1], 16) * 0x100 + int(input_md4[j][0], 16)
    input_md4[0] = (input_md4[0] - 0x67452301) & MD4.mask
    input_md4[1] = (input_md4[1] - 0xEFCDAB89) & MD4.mask
    input_md4[2] = (input_md4[2] - 0x98BADCFE) & MD4.mask
    input_md4[3] = (input_md4[3] - 0x10325476) & MD4.mask
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
    expected = input_md4.copy()
    MD4.reverse(expected, x1, x2)

    for x0 in range(0xFFFFFFFF + 1):
        s1 = struct.pack("<L", x0) + s
        x = list(struct.unpack("<16I", s1))
        x[0] = x0
        x1[0] = (x1[0] + 1) & MD4.mask
        x2[0] = (x2[0] + 1) & MD4.mask
        if MD4.hash_optimized_compare(input_md4, x, x1, x2, expected):
            print("preimage founded: " + s1[0:s_len].hex())


def inner_loop_0(input_md4):  # x1 = 00000000 (length changeable)
    input_md4 = [input_md4[i: i + 8] for i in range(0, 32, 8)]
    for i in range(4):
        input_md4[i] = [input_md4[i][0:2], input_md4[i][2:4], input_md4[i][4:6], input_md4[i][6:8]]
    for j in range(4):
        input_md4[j] = int(input_md4[j][3], 16) * 0x1000000 + int(input_md4[j][2], 16) * 0x10000 + \
                       int(input_md4[j][1], 16) * 0x100 + int(input_md4[j][0], 16)
    input_md4[0] = (input_md4[0] - 0x67452301) & MD4.mask
    input_md4[1] = (input_md4[1] - 0xEFCDAB89) & MD4.mask
    input_md4[2] = (input_md4[2] - 0x98BADCFE) & MD4.mask
    input_md4[3] = (input_md4[3] - 0x10325476) & MD4.mask
    x = [0] * 16
    x1 = [0x5A827999] * 16
    x2 = [0x6ED9EBA1] * 16
    x[0] = 128
    x1[0] += 128
    x2[0] += 128
    if MD4.hash_compare(input_md4, x, x1, x2):
        print("preimage founded: " + hex(x[0]))
    x[0] = 0
    x1[0] = 0x5A827999
    x2[0] = 0x6ED9EBA1
    x[1] = 128
    x1[1] = 0x5A827999 + 128
    x2[1] = 0x6ED9EBA1 + 128
    x[14] = 32
    x1[14] = 0x5A827999 + 32
    x2[14] = 0x6ED9EBA1 + 32
    expected = input_md4.copy()
    MD4.reverse(expected, x1, x2)
    for c in range(0xFFFFFFFF):
        x[0] += 1
        x1[0] = (x1[0] + 1) & MD4.mask
        x2[0] = (x2[0] + 1) & MD4.mask
        if MD4.hash_optimized_compare(input_md4, x, x1, x2, expected):
            print("preimage founded: " + hex(x[0]))
            return 1
    return 0


def work(input_md4):
    processes = [Process()] * NUMBER_OF_PROCESSES
    # outer loop
    proc = Process(target=inner_loop_0, args=tuple([input_md4]))
    processes[0] = proc
    proc.start()
    for x1 in range(1, 0xFFFFFFFF + 1, 1):
        if x1 % NUMBER_OF_PROCESSES == NUMBER_OF_PROCESSES - 1:
            for proc in processes:
                proc.join()
        x1b = struct.pack("<L", x1)
        proc = Process(target=inner_loop, args=(x1b, input_md4))
        processes[x1 % NUMBER_OF_PROCESSES] = proc
        proc.start()
