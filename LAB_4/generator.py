import argparse
import random
import string
import time

allowed_chars = string.ascii_letters + string.punctuation

def parse():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-sn", help="Substrings number in file 'substrings'", default=20)
    group.add_argument("-ss", help="Substrings size", default=10)
    group.add_argument("-ts", help="Text size in KB", default=5)
    parser.add_argument("-f", help="The frequency of occurrence of the substring", default=5)
    args = parser.parse_args()
    return args


def generate_substrings(n, str_size):
    strs = []
    for i in range(n):
        s = ''.join(random.choice(allowed_chars) for j in range(str_size))
        while strs.__contains__(s) != 0:
            s = ''.join(random.choice(allowed_chars) for j in range(str_size))
        strs.append(s)
    return strs


def save_subs(data, filename):
    with open(filename, 'w') as f:
        for s in data:
            f.write(s + '\n')
    f.close()


def save_text(txt_size, subs, freq, filename):
    block_size = len(subs[0])
    txt_size = int(txt_size * 1024 / block_size)
    additional_symbols = (txt_size * 1024) % block_size
    c = c1 = 100       # how many blocks should be written in 1 iteration
    r = 100
    while freq % 1 != 0:
        freq *= 10
        r *= 10
    text_part = ''
    with open(filename, 'w') as f:
        for i in range(int(txt_size/c1) + 1):
            if i == int(txt_size/c1):
                c = txt_size % c1
            for j in range(c):
                if random.randint(1, r) <= freq:
                    block = random.choice(subs)
                else:
                    block = ''.join(random.choice(allowed_chars) for k in range(block_size))
                    while subs.__contains__(block) != 0:
                        block = ''.join(random.choice(allowed_chars) for k in range(block_size))
                text_part += block
            f.write(text_part)
            text_part = ''
        block = ''.join(random.choice(allowed_chars) for k in range(additional_symbols))
        f.write(block)
    f.close()


args = parse()
substrings = generate_substrings(args.sn, args.ss)
save_subs(substrings, 'substrings.txt')
t = time.time_ns()
save_text(args.ts, substrings, args.f, 'text.txt')
t = time.time_ns() - t
print('Time: %0.9f' % (float(t / 1000000000.0)) + ' seconds')
