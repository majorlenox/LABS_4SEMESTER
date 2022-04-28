import struct

from md4 import MD4

md = MD4()

def make_block(s):
    if type(s) == str:
        s = bytearray(s, 'utf-8')
    s_len = len(s)
    s += b"\x80"
    s += b'\x00' * (56 - len(s))
    s += struct.pack("<L", s_len * 8) + b'\x00' * 4
    return s

to_hash = b'The quick brown fox jumps over the lazy dog'
x = make_block(to_hash)
#for i in range(0, len(to_hash), 64):
#    print(list(struct.unpack("<16I", x[i: i + 64])))
print(md.md4_hash(x).hex())
