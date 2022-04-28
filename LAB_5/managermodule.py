import struct
from multiprocessing import Process

from md4 import MD4

NUMBER_OF_PROCESSES = 4

md = MD4()


def inner_loop(x0, input_md4):
    for x1 in range(0xFFFFFFFF + 1):
        s = x0 + struct.pack("<L", x1)
        s_len = get_length(s)
        if s_len != 0:
            if len(bin(s[s_len - 1])) - 3 != -1:
                mask_1 = pow(2, len(bin(s[s_len - 1])) - 3)
                s = s[:s_len - 1] + bytes([s[s_len - 1] | mask_1]) + s[s_len:]
            else:
                s += b'\x80'
        else:
            s = b'\x80' + b'\x00' * 7
        s += b'\x00' * (56 - len(s))
        s += struct.pack("<L", s_len) + b'\x00' * 4
        if md.md4_optimized_compare(s, input_md4) == 1:
            print("preimage founded: " + s[0:s_len].hex())


def get_length(s):
    s = struct.unpack("<8c", s)
    k = 7
    while (k >= 0) & (s[k] == b"\x00"):
        k -= 1
    return k + 1


def work(input_md4):
    processes = [Process()] * NUMBER_OF_PROCESSES
    # outer loop
    for x0 in range(0xFFFFFFFF + 1):
        x0b = struct.pack("<L", x0)
        proc = Process(target=inner_loop, args=(x0b, input_md4))
        processes[x0 % NUMBER_OF_PROCESSES] = proc
        proc.start()
        if x0 % NUMBER_OF_PROCESSES == NUMBER_OF_PROCESSES - 1:
            for proc in processes:
                proc.join()
