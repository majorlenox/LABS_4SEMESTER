import struct

from md4 import MD4



#to_hash = b'The quick brown fox jumps over the lazy dog'
to_hash = b'123'
x = MD4.make_block(to_hash)
print(MD4.hash(x).hex())
