class MD4:
    width = 32
    mask = 0xFFFFFFFF

    @staticmethod
    def F(x1, x2, x3):
        return x1 & x2 | ((~x1) & x3)

    @staticmethod
    def G(x1, x2, x3):
        return x1 & x2 | x1 & x3 | x2 & x3

    @staticmethod
    def H(x1, x2, x3):
        return x1 ^ x2 ^ x3

    @staticmethod
    def lrot(x1, s):
        l = (x1 << s) & MD4.mask
        r = x1 >> (MD4.width - s)
        return l | r

    @staticmethod
    def STEP(func, a, b, c, d, k, s, x):
        return MD4.lrot(a + func(b, c, d) + x[k], s)

    def md4_hash(self, x):
        reg = [] * 4  # reg[0] = A, reg[1] = B, reg[2] = C, reg[3] = D
        reg[0] = AA = 0x01234567
        reg[1] = BB = 0x89abcdef
        reg[2] = CC = 0xfedcba98
        reg[3] = DD = 0x76543210

        x1 = x2 = [] * 16
        for i in range(16):
            x1[i] = (x[i] + 0x5A827999) % MD4.mask
            x2[i] = (x[i] + 0x6ED9EBA1) % MD4.mask

        for i in range(16):

            # round 1
            s = [3, 7, 11, 19]
            for j in range(16):
                reg[3 * j % 4] = MD4.STEP(self.F, reg[3 * j % 4], reg[(1 + 3 * j) % 4], reg[(2 + 3 * j) % 4],
                                          reg[(3 + 3 * j) % 4], j, s[j % 4], x)

            # round 2
            s = [3, 5, 9, 13]
            for j in range(16):
                reg[3 * j % 4] = MD4.STEP(self.G, reg[3 * j % 4], reg[(1 + 3 * j) % 4], reg[(2 + 3 * j) % 4],
                                          reg[(3 + 3 * j) % 4], (j % 4) * 4 + j / 4, s[j % 4], x1)
            # round 3
            s = [3, 9, 11, 15]
            for j in range(16):
                reg[3 * j % 4] = MD4.STEP(self.H, reg[3 * j % 4], reg[(1 + 3 * j) % 4], reg[(2 + 3 * j) % 4],
                                          reg[(3 + 3 * j) % 4], (j % 4) / 2 * 4 + (j % 2) * 8 + (j / 4) * 2, s[j % 4],
                                          x2)
            reg[0] += AA
            reg[1] += BB
            reg[2] += CC
            reg[3] += DD

        return str(reg[0]) + str(reg[1]) + str(reg[2]) + str(reg[3])