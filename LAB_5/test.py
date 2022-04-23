def make_block(s):
    x = [0] * 16
    s_length = len(s)
    for i in range(0, int(s_length/4) * 4, 4):
        x[int(i/4)] = ord(s[i])*0x01000000 + ord(s[i + 1])*0x00010000 + ord(s[i + 2])*0x00000100 + ord(s[i + 3])
    t = 0x01000000
    k = s_length - int(s_length/4) * 4
    j = 0
    while k != 0:
        x[int(s_length/4)] += ord(s[int(s_length/4) + j]) * t
        t = t >> 8
        k -= 1
        j += 1
    x[int(s_length / 4)] += 1 * t << 7                  # msg + 1000...000
    return x

to_hash = 'dasdaadsdces'
x = make_block(to_hash)
for i in range(16):
    print(str(x[i]) + " = " + format(x[i], '032b'))
