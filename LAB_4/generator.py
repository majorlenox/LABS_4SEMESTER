import argparse
import random
import string
import time

allowed_chars = string.ascii_letters + string.punctuation


def parse():
    parser = argparse.ArgumentParser()
    group = parser.add_argument_group()
    group.add_argument("-sn", help="Substrings number in file 'substrings.txt'", default=10, type=int)
    group.add_argument("-ss", help="Substrings size", default=10, type=int)
    group.add_argument("-ts", help="Text size in Bytes", default=1000, type=int)
    parser.add_argument("-f", help="The frequency of occurrence of the substring", default=10, type=int)
    args = parser.parse_args()
    return args


def generate_substrings(n, line_size):
    strs = []
    for i in range(n):
        s = ''.join(random.choice(allowed_chars) for j in range(line_size))
        while strs.__contains__(s) != 0:
            s = ''.join(random.choice(allowed_chars) for j in range(line_size))
        strs.append(s)
    return strs


def save_subs(data, filename):
    with open(filename, 'w') as f:
        for s in data:
            f.write(s + '\n')
    f.close()


def save_text(txt_size, subs, freq, filename):
    block_size = len(subs[0])
    freq = freq/block_size
    r = 100
    while freq % 1 != 0:
        freq *= 10
        r *= 10
    freq = int(freq)
    with open(filename, 'w') as f:
        block = ''
        while txt_size:
            if random.randint(1, r) <= freq:
                substring = random.choice(subs)
                if txt_size < block_size:
                    block += substring[0: txt_size - 1]
                    txt_size = 0
                else:
                    block += substring
                    txt_size -= block_size
                f.write(block)
                block = ''
            else:
                block += random.choice(allowed_chars)
                txt_size -= 1
        f.write(block)
    f.close()


args = parse()
substrings = generate_substrings(args.sn, args.ss)
save_subs(substrings, 'substrings.txt')
t = time.time_ns()
save_text(args.ts, substrings, args.f, 'text.txt')
t = time.time_ns() - t
print('Time: %0.9f' % (float(t / 1000000000.0)) + ' seconds')
