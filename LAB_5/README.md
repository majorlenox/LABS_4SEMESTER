- создать полноценный md4 hash
- STEP_REV
- начать откручивать
- возможность выйти раньше если A,B,C,D не совпали

- Resources:
  - https://github.com/hashcat/hashcat/blob/master/OpenCL/m01000_a3-optimized.cl
  - https://ru.wikipedia.org/wiki/MD4
  - 
  - 
    def make_block(s):
        if type(s) == str:
            s = bytearray(s, 'utf-8')
        s_len = 0
        sb_len = 0
        if s != b'':
            s_len = MD4.get_length(s)
            sb_len = (s_len - 1) * 8
        if s_len == 0:
            s = b'\x80'
            sb_len = 0
        else:
            if s[s_len - 1] % 2 != 0:
                s += b'\x80'
                sb_len += 8
            else:
                b, k = MD4.add_1(s[s_len - 1])
                s = s[:s_len - 1] + bytes([b])
                sb_len += k + 1
        s += b'\x00' * (56 - len(s) % 64)
        s += struct.pack("<L", sb_len & MD4.mask) + struct.pack("<L", sb_len // MD4.mask)
        return s