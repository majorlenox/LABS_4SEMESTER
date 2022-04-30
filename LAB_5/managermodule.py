import struct
from multiprocessing import Process, Pool

from md4 import MD4

NUMBER_OF_PROCESSES = 4


def inner_loop(v):
    input_md4, mode = v                   # mode a also x[1] !
    input_md4 = MD4.read_hash(input_md4)
    x = [0] * 16
    x1 = [0x5A827999] * 16
    x2 = [0x6ED9EBA1] * 16
    configure_x(mode, x, x1, x2)
    expected = input_md4.copy()
    MD4.reverse(expected, x1, x2)
    for c in range(0xFFFFFFFF):
        x[0] += 1
        x1[0] = (x1[0] + 1) & MD4.mask
        x2[0] = (x2[0] + 1) & MD4.mask
        if MD4.hash_optimized_compare(input_md4, x, x1, x2, expected):
            print("preimage founded: " + str(struct.pack("<2L", x[0], x[1])))
            return 1
    return 0


def configure_x(m, x, x1, x2):
    if m == 0:                      # 1 byte configuration ( only x0 )
        x[1] = 128
        x1[1] = 0x5A827999 + 128
        x2[1] = 0x6ED9EBA1 + 128
        x[14] = 32
        x1[14] = 0x5A827999 + 32
        x2[14] = 0x6ED9EBA1 + 32
    else:                           # 2 byte configuration ( x0 and x1)
        x[1] = m
        x1[1] = 0x5A827999 + m
        x2[1] = 0x6ED9EBA1 + m
        x[2] = 128
        x1[2] = 0x5A827999 + 128
        x2[2] = 0x6ED9EBA1 + 128
        x[14] = 64
        x1[14] = 0x5A827999 + 64
        x2[14] = 0x6ED9EBA1 + 64
    return


def work(input_md4):
    if MD4.hash_compare(input_md4, [128] + [0] * 15, [0x5A827999 + 128] + [0x5A827999] * 15,
                        [0x6ED9EBA1 + 128] + [0x6ED9EBA1] * 15):  # zero check
        print("preimage founded: b''")
        return 1
    flag = 0
    args = [[input_md4, 0] for i in range(NUMBER_OF_PROCESSES)]
    # Outer loop
    x1 = 1
    while x1 <= 0xFFFFFFFF:
        with Pool(processes=NUMBER_OF_PROCESSES) as pool:
            for j in range(NUMBER_OF_PROCESSES):
                if x1 <= 0xFFFFFFFF:
                    args[j][1] = x1
                    x1 += 1
            for r in pool.imap_unordered(inner_loop, args):
                if r:
                    pool.terminate()
                    flag = True
                    return 0
    if not flag:
        print('There is no preimage')
    return 0