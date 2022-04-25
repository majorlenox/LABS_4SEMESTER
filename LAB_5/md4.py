import struct


def make_block(s):
    if type(s) == str:
        s = bytearray(s, 'utf-8')
    s_len = len(s)
    s += b"\x80"
    s += b'\x00' * (56 - len(s))
    s += struct.pack("<L", s_len * 8) + b'\x00' * 4
    return s


class MD4:
    width = 32
    mask = 0xFFFFFFFF

    @staticmethod
    def F(x1, x2, x3):
        return (x1 & x2) | ((~x1) & x3)

    @staticmethod
    def G(x1, x2, x3):
        return x1 & x2 | x1 & x3 | x2 & x3

    @staticmethod
    def H(x1, x2, x3):
        return x1 ^ x2 ^ x3

    @staticmethod
    def lrot(x1, s):
        l, r = (x1 << s) & MD4.mask, x1 >> (MD4.width - s)
        return l | r

    @staticmethod
    def STEP(func, a, b, c, d, k, s, x):
        return MD4.lrot((a + func(b, c, d) + x[k]) & MD4.mask, s)

    def md4_hash(self, s):
        x = list(struct.unpack("<16I", s))

        reg = [0] * 4  # reg[0] = A, reg[1] = B, reg[2] = C, reg[3] = D
        reg[0] = AA = 0x67452301
        reg[1] = BB = 0xEFCDAB89
        reg[2] = CC = 0x98BADCFE
        reg[3] = DD = 0x10325476

        x1 = [0] * 16
        x2 = [0] * 16
        for i in range(16):
            x1[i] = (x[i] + 0x5A827999) & MD4.mask
            x2[i] = (x[i] + 0x6ED9EBA1) & MD4.mask

            # round 1
        s = [3, 7, 11, 19]
        for j in range(16):
            reg[3 * j % 4] = MD4.STEP(self.F, reg[3 * j % 4], reg[(1 + 3 * j) % 4], reg[(2 + 3 * j) % 4],
                                      reg[(3 + 3 * j) % 4], j, s[j % 4], x)
            # round 2
        s = [3, 5, 9, 13]
        for j in range(16):
            reg[3 * j % 4] = MD4.STEP(self.G, reg[3 * j % 4], reg[(1 + 3 * j) % 4], reg[(2 + 3 * j) % 4],
                                      reg[(3 + 3 * j) % 4], (j % 4) * 4 + j // 4, s[j % 4], x1)
            # round 3
        s = [3, 9, 11, 15]
        r = [0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15]
        for j in range(16):
            reg[3 * j % 4] = MD4.STEP(self.H, reg[3 * j % 4], reg[(1 + 3 * j) % 4], reg[(2 + 3 * j) % 4],
                                      reg[(3 + 3 * j) % 4], r[j], s[j % 4], x2)

        reg[0] = (reg[0] + AA) & self.mask
        reg[1] = (reg[1] + BB) & self.mask
        reg[2] = (reg[2] + CC) & self.mask
        reg[3] = (reg[3] + DD) & self.mask

        return struct.pack("<L", reg[0]) + struct.pack("<L", reg[1]) + struct.pack("<L", reg[2]) + \
               struct.pack("<L", reg[3])
