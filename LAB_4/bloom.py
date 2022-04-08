import math
import mmh3


class bloom_filter:

    def __init__(self, , m):
        m *= 8

        k = int(m/n * math.log(2))
        s = []

