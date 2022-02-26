import hashlib
import multiprocessing
import os.path
import random
import time
from multiprocessing import Process, Pipe
from threading import Thread


def greater(a, b):  # increasing
    return a < b


def less(a, b):     # decreasing
    return a > b


def partition_greater(array, begin, end):
    pivot = begin
    l, r = begin, end
    while True:
        while (array[r][0] >= array[pivot][0]) & (l < r):
            r -= 1
        while (array[l][0] <= array[pivot][0]) & (l < r):
            l += 1
        if l < r:
            array[l], array[r] = array[r], array[l]
        else:
            break

    array[pivot], array[l] = array[l], array[pivot]

    return r


def partition_less(array, begin, end):
    pivot = end
    l, r = begin, end
    while True:
        while (array[l][0] >= array[pivot][0]) & (l < r):
            l += 1
        while (array[r][0] <= array[pivot][0]) & (l < r):
            r -= 1
        if l < r:
            array[l], array[r] = array[r], array[l]
        else:
            break

    array[pivot], array[l] = array[l], array[pivot]

    return l


def quick_sort_greater(array, begin, end):
    if begin >= end:
        return
    p = partition_greater(array, begin, end)
    quick_sort_greater(array, begin, p - 1)
    quick_sort_greater(array, p + 1, end)


def quick_sort_less(array, begin, end):
    if begin >= end:
        return
    p = partition_less(array, begin, end)
    quick_sort_less(array, begin, p - 1)
    quick_sort_less(array, p + 1, end)


def quick_sort_ret(array, begin, end, return_dict):
    numbers = array.copy()
    quick_sort_greater(array, begin, end)
    return_dict[5] = proc1.get_duration()
    return_dict[0] = array
    quick_sort_less(numbers, begin, end)
    return_dict[6] = proc1.get_duration() - return_dict[5]
    return_dict[1] = numbers


def merge_sort_ret(array, begin, end, return_dict):
    return_dict[2] = merge_sort(array, begin, end, greater)
    return_dict[7] = proc2.get_duration()
    return_dict[3] = merge_sort(array, begin, end, less)
    return_dict[8] = proc2.get_duration() - return_dict[7]


def merge_sort(array, begin, end, comparator):
    if begin - end == 0:
        return [array[begin]]
    m = int((begin + end) / 2)
    l = merge_sort(array, begin, m, comparator)
    r = merge_sort(array, m + 1, end, comparator)
    return merge(l, r, comparator)


def merge(l, r, comparator):
    result = [None] * (len(l) + len(r))
    i, j = 0, 0
    while (i < len(l)) & (j < len(r)):
        if comparator(l[i][0], r[j][0]):
            result[i + j] = l[i]
            i += 1
        else:
            result[i + j] = r[j]
            j += 1

    while j != len(r):
        result[i + j] = r[j]
        j += 1
    while i != len(l):
        result[i + j] = l[i]
        i += 1
    return result


def generate_sha1_file(n):
    sha1_file = open("./SHA1.txt", 'w+')
    for i in range(n):
        hash_object = hashlib.sha1(random.randbytes(1000))
        if i != n - 1:
            sha1_file.write(hash_object.hexdigest() + '\n')
        else:
            sha1_file.write(hash_object.hexdigest())
    sha1_file.close()


def from_sha1_to_numbers(sha1_array):
    numbers = []  # every 16 hex (64 bits) becomes one decimal number (from 0 to 2^64 - 1)
    for sha1 in sha1_array:
        numbers.append((int(sha1[0:16], 16), sha1))
    return numbers


class TimedProcess(Process):
    daemon = True

    def __init__(self, *args, **kwargs):
        super(TimedProcess, self).__init__(*args, **kwargs)
        self.parent_conn, self.child_conn = Pipe()
        self.child_finished = False
        self._duration = 0.0

    def get_duration(self):
        if not self.child_finished:
            self.parent_conn.send(None)
            result = self.parent_conn.recv()
            if result == 'done':
                self.child_finished = True
            else:
                self._duration = result
        return self._duration

    def run(self):
        try:
            t0 = time.process_time_ns()
            Thread(target=self._run).start()
            while True:
                request = self.child_conn.recv()
                self.child_conn.send(time.process_time_ns() - t0)
                if request == 'stop':
                    break
        finally:
            self.child_conn.send('done')

    def _run(self):
        try:
            super(TimedProcess, self).run()
        finally:
            self.parent_conn.send('stop')


# main

c = 1

while c != '0':
    print("Choose action:\n 0 - Quit\n 1 - Generate new SHA1 file\n 2 - Select the SHA1 file and sort it")
    c = input()
    if c == '1':
        print("Enter number of SHA1 (one SHA1 has 160 bits)")
        n = input()
        generate_sha1_file(int(n))
        print("New file ./SHA1.txt was created")
    if c == '2':
        print("Enter path to SHA1 file\n Example: ./SHA1.txt")
        sha1_path = input()
        if not os.path.exists(sha1_path):
            print("This file does not exist!")
        else:
            file = open(sha1_path, 'r')
            sha1_unsorted = file.read().split('\n')
            file.close()

            sha1_n_pair = from_sha1_to_numbers(sha1_unsorted)
            # for number, sha1 in sha1_n_pair:
            #     print(str(number) + " " + str(sha1))

            manager = multiprocessing.Manager()
            return_dict = manager.dict()
            proc1 = TimedProcess(target=quick_sort_ret, args=(sha1_n_pair, 0, len(sha1_n_pair) - 1, return_dict))
            proc2 = TimedProcess(target=merge_sort_ret, args=(sha1_n_pair, 0, len(sha1_n_pair) - 1, return_dict))
            proc1.start()
            proc2.start()
            proc1.join()
            proc2.join()

            file = open("./SHA1_sorted_qsGreater.txt", "w")
            for sha1 in return_dict[0]:
                file.write(str(sha1[1]) + '\n')
            file.write('\n Quick sort greater, time: ' + str(return_dict[5] / 1000000000) + 's\n')
            file.close()

            file = open("./SHA1_sorted_qsLess.txt", "w")
            for sha1 in return_dict[1]:
                file.write(str(sha1[1]) + '\n')
            file.write('\n Quick sort less, time: ' + str(return_dict[6] / 1000000000) + 's\n')
            file.close()

            file = open("./SHA1_sorted_msGreater.txt", "w")
            for sha1 in return_dict[2]:
                file.write(str(sha1[1]) + '\n')
            file.write('\n Merge sort greater, time: ' + str(return_dict[7] / 1000000000) + 's\n')
            file.close()

            file = open("./SHA1_sorted_msLess.txt", "w")
            for sha1 in return_dict[3]:
                file.write(str(sha1[1]) + '\n')
            file.write('\n Merge sort greater, time: ' + str(return_dict[8] / 1000000000) + 's\n')
            file.close()

            print("Sorted sha1 were saved in ./SHA1_sorted.txt")
