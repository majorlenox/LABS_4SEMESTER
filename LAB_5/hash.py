from md4 import MD4

to_hash = b'\x1A\xC1\x00\x00\x03\x00\x00\x00'
x = MD4.make_block(to_hash)
print(MD4.hash(x).hex())

