import struct
import hashlib

def make_block(s):
    if type(s) == str:
        s = bytearray(s, 'utf-8')
    ml = len(s) * 8
    s += b"\x80"
    s += b"\x00" * (56 - len(s) % 64)
    s += struct.pack("<Q", ml)
    return s

x0b = struct.pack("<c", bytes([3]))
print(x0b)
#print(struct.pack('<L', 1233333333))
to_hash = 'wasdwasdwasd'
x = make_block(to_hash)
for i in range(0, len(to_hash), 64):
    print(list(struct.unpack("<16I", x[i: i + 64])))
