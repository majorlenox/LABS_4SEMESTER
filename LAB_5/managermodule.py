import struct
from multiprocessing import Process

NUMBER_OF_PROCESSES = 4


def inner_loop(x0):
    for x1 in range(0xFFFFFFFF + 1):
        s = x0 + struct.pack("<L", x1)
        s_len = get_length(s)
        if s_len == 0:
            print("BRUH")
        if s_len != 0:
            if len(bin(s[s_len - 1])) - 3 != -1:
                mask_1 = pow(2, len(bin(s[s_len - 1])) - 3)
                #print(bytes(hex(s[s_len - 1] | mask_1).removeprefix('0'), 'utf-8'))
                print(mask_1)
                #print(struct.pack("<1c", bytes([s[s_len - 1] | mask_1])))
                s = s[:s_len - 1] + bytes([s[s_len - 1] | mask_1]) + s[s_len:]
            else:
                s += b'\x80'
        else:
            s = b'\x80' + b'\x00' * 7
      #  image = s + b"\x00" * 48 +


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
        # x1b = format(x1, '#034b').removeprefix('0b')
        proc = Process(target=inner_loop, args=tuple([x0b]))
        processes[x0 % NUMBER_OF_PROCESSES] = proc
        proc.start()
        if x0 % NUMBER_OF_PROCESSES == NUMBER_OF_PROCESSES - 1:
            for proc in processes:
                proc.join()
