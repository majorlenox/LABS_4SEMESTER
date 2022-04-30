import struct


class MD4:
    width = 32
    mask = 0xFFFFFFFF

    @staticmethod
    def make_block(s):
        if type(s) == str:
            s = bytearray(s, 'utf-8')
        if s == b'':
            s = b"\x80"
            l = 0
        else:
            l = MD4.get_length(s)
            s += b"\x80"
        s += b'\x00' * (56 - len(s) % 64)
        s += struct.pack("<L", l & MD4.mask) + struct.pack("<L", l // MD4.mask)
        return s

    @staticmethod
    def get_length(s):
        s = struct.unpack("<" + str(len(s)) + "c", s)
        return len(s)*8

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
    def rrot(x1, s):
        l, r = x1 >> s, (x1 << (MD4.width - s)) & MD4.mask
        return l | r

    @staticmethod
    def STEP(func, a, b, c, d, k, s, x):
        return MD4.lrot((a + func(b, c, d) + x[k]) & MD4.mask, s)

    @staticmethod
    def STEP_REV(func, a, b, c, d, k, s, x):
        return (MD4.rrot(a, s) - x[k] - func(b, c, d)) & MD4.mask

    @staticmethod
    def STEP_REV1(a, k, s, x):
        return (MD4.rrot(a, s) - x[k]) & MD4.mask

    @staticmethod
    def hash(to_hash):

        reg = [0] * 4  # reg[0] = A, reg[1] = B, reg[2] = C, reg[3] = D
        reg[0] = 0x67452301
        reg[1] = 0xEFCDAB89
        reg[2] = 0x98BADCFE
        reg[3] = 0x10325476

        for c in range(0, len(to_hash), 64):

            AA = reg[0]
            BB = reg[1]
            CC = reg[2]
            DD = reg[3]

            x = list(struct.unpack("<16I", to_hash[c:c + 64]))

            x1 = [0] * 16
            x2 = [0] * 16
            for i in range(16):
                x1[i] = (x[i] + 0x5A827999) & MD4.mask
                x2[i] = (x[i] + 0x6ED9EBA1) & MD4.mask

                # round 1
            s = [3, 7, 11, 19]
            for j in range(16):
                reg[3 * j % 4] = MD4.STEP(MD4.F, reg[3 * j % 4], reg[(1 + 3 * j) % 4], reg[(2 + 3 * j) % 4],
                                          reg[(3 + 3 * j) % 4], j, s[j % 4], x)
                # round 2
            s = [3, 5, 9, 13]
            for j in range(16):
                reg[3 * j % 4] = MD4.STEP(MD4.G, reg[3 * j % 4], reg[(1 + 3 * j) % 4], reg[(2 + 3 * j) % 4],
                                          reg[(3 + 3 * j) % 4], (j % 4) * 4 + j // 4, s[j % 4], x1)
                # round 3
            s = [3, 9, 11, 15]
            r = [0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15]
            for j in range(16):
                reg[3 * j % 4] = MD4.STEP(MD4.H, reg[3 * j % 4], reg[(1 + 3 * j) % 4], reg[(2 + 3 * j) % 4],
                                          reg[(3 + 3 * j) % 4], r[j], s[j % 4], x2)

            reg[0] = (reg[0] + AA) & MD4.mask
            reg[1] = (reg[1] + BB) & MD4.mask
            reg[2] = (reg[2] + CC) & MD4.mask
            reg[3] = (reg[3] + DD) & MD4.mask

        return struct.pack("<L", reg[0]) + struct.pack("<L", reg[1]) + struct.pack("<L", reg[2]) + \
               struct.pack("<L", reg[3])

    @staticmethod
    def hash_optimized_compare(input_hash, x, x1, x2, expected):
        reg = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476]  # reg[0] = A, reg[1] = B, reg[2] = C, reg[3] = D

        expected[0] -= x[0]
        expected[1] -= expected[1] - MD4.G(expected[4], expected[3], expected[0])
        expected[2] -= MD4.G(expected[3], expected[0], expected[1])

        # round 1
        s = [3, 7, 11, 19]
        for j in range(16):
            reg[3 * j % 4] = MD4.STEP(MD4.F, reg[3 * j % 4], reg[(1 + 3 * j) % 4], reg[(2 + 3 * j) % 4],
                                      reg[(3 + 3 * j) % 4], j, s[j % 4], x)
        # round 2
        s = [3, 5, 9, 13]
        for j in range(0, 11):
            reg[3 * j % 4] = MD4.STEP(MD4.G, reg[3 * j % 4], reg[(1 + 3 * j) % 4], reg[(2 + 3 * j) % 4],
                                      reg[(3 + 3 * j) % 4], (j % 4) * 4 + j // 4, s[j % 4], x1)
        if reg[2] != expected[2]:
            return 0
        reg[1] = MD4.STEP(MD4.G, reg[1], reg[2], reg[3], reg[0], 14, 13, x1)
        if reg[1] != expected[1]:
            return 0
        reg[0] = MD4.STEP(MD4.G, reg[0], reg[1], reg[2], reg[3], 3, 3, x1)
        if reg[0] != expected[0]:
            return 0
        for j in range(13, 16):
            reg[3 * j % 4] = MD4.STEP(MD4.G, reg[3 * j % 4], reg[(1 + 3 * j) % 4], reg[(2 + 3 * j) % 4],
                                      reg[(3 + 3 * j) % 4], (j % 4) * 4 + j // 4, s[j % 4], x1)

        # round 3
        s = [3, 9, 11, 15]
        r = [0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15]
        for j in range(1, 16, 1):
            reg[3 * j % 4] = MD4.STEP(MD4.H, reg[3 * j % 4], reg[(1 + 3 * j) % 4], reg[(2 + 3 * j) % 4],
                                      reg[(3 + 3 * j) % 4], r[j], s[j % 4], x2)

        if reg == input_hash:
            return 1
        return 0

    @staticmethod
    def hash_compare(input_hash, x, x1, x2):
        reg = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476]  # reg[0] = A, reg[1] = B, reg[2] = C, reg[3] = D

            # round 1
        s = [3, 7, 11, 19]
        for j in range(16):
            reg[3 * j % 4] = MD4.STEP(MD4.F, reg[3 * j % 4], reg[(1 + 3 * j) % 4], reg[(2 + 3 * j) % 4], reg[(3 + 3 * j) % 4], j, s[j % 4], x)

            # round 2
        s = [3, 5, 9, 13]
        for j in range(16):
            reg[3 * j % 4] = MD4.STEP(MD4.G, reg[3 * j % 4], reg[(1 + 3 * j) % 4], reg[(2 + 3 * j) % 4],
                                      reg[(3 + 3 * j) % 4], (j % 4) * 4 + j // 4, s[j % 4], x1)
            # round 3
        s = [3, 9, 11, 15]
        r = [0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15]
        for j in range(16):
            reg[3 * j % 4] = MD4.STEP(MD4.H, reg[3 * j % 4], reg[(1 + 3 * j) % 4], reg[(2 + 3 * j) % 4],
                                      reg[(3 + 3 * j) % 4], r[j], s[j % 4], x2)

        if reg == input_hash:
            return 1
        return 0

    @staticmethod
    def reverse(reg, x1, x2):
        s = [3, 9, 11, 15]
        r = [0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15]
        # rev round 3
        for j in range(15, -1, -1):
            reg[3 * j % 4] = MD4.STEP_REV(MD4.H, reg[3 * j % 4], reg[(1 + 3 * j) % 4], reg[(2 + 3 * j) % 4],
                                          reg[(3 + 3 * j) % 4], r[j], s[j % 4], x2)
        reg.append(reg[2])  # save C

        # rev round 2
        reg[1] = MD4.STEP_REV1(reg[1], 15, 13, x1)
        reg[2] = MD4.STEP_REV1(reg[2], 11, 9, x1)

        return reg
