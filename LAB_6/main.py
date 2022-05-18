import argparse
import os
import time

import matrix
import strassen

DEFAULT_FILENAME = './matrices.txt'


def parse():
    parser = argparse.ArgumentParser()
    group1 = parser.add_argument_group()
    group2 = parser.add_argument_group()
    group1.add_argument("-f", help="Matrix from file", default="", nargs='?', type=str)
    group2.add_argument('-n', help='The number of rows in matrix 1 to generate', action='store', type=int)
    group2.add_argument('-mn', help='The number of columns in matrix 1 and rows in matrix 2 to generate',
                        action='store', type=int)
    group2.add_argument('-m', help='The number of columns in matrix 2 to generate', action='store', type=int)
    group2.add_argument('-s', help='Will the generated matrices be saved', action='store_true', default=False)
    group2.add_argument('-d', help='Display matrices A,B,C to stdout', action='store_true', default=False)
    return parser.parse_args()


class args:
    f = ""
    n = 1000
    mn = 1000
    m = 1000
    s = False
    d = False


if __name__ == '__main__':
    #args = parse()
    if args.f != "":
        if args.f is None:
            args.f = DEFAULT_FILENAME
        if not os.path.exists(args.f):
            print("These file doesn't exist!")
            exit(-2)
        matrix_a, matrix_b = matrix.load_matrices(args.f)
        if matrix_a is None:
            exit(1)
        print("Matrices were loaded from file " + args.f)
    else:
        if (args.n is None) | (args.mn is None) | (args.m is None):
            print("Use the -f flag to specify the path to the matrices file, or use flags -n, -nm and -m to generate"
                  " matrices of a set size")
            exit(1)
        matrix_a, matrix_b = matrix.generate_matrices(args.n, args.mn, args.m)
        if args.s:
            matrix.save_matrices(matrix_a, matrix_b, DEFAULT_FILENAME)
            print("A file with matrices was created in ./matrix.txt")
    t = time.time_ns()
    matrix_1 = matrix.multiply_matrices(matrix_a, matrix_b)
    #matrix.save_result_matrix(matrix_1, "./result_trivial.txt")
    t = time.time_ns() - t
    if args.d:
        print("Matrix A:")
        matrix.show_matrix(matrix_a)
        print("Matrix B:")
        matrix.show_matrix(matrix_b)
        print("Result matrix C: ")
        matrix.show_matrix(matrix_1)
    print('Trivial multiplication: %0.9f' % (float(t / 1000000000.0)) + ' seconds')
    t = time.time_ns()
    matrix_2 = strassen.work_np(matrix_a, matrix_b)
    t = time.time_ns() - t
    if args.d:
        matrix.show_matrix(matrix_2)
    print('Strassen algorithm: %0.9f' % (float(t / 1000000000.0)) + ' seconds')
    t = time.time_ns()
    t = time.time_ns() - t
    if args.d:
        matrix.show_matrix(matrix_2)
    print('Strassen algorithm on multiprocessing: %0.9f' % (float(t / 1000000000.0)) + ' seconds')
    #matrix.compare_three(m)
    if matrix.compare_three_matrices(matrix_1, matrix_2, matrix_2):
        print("Matrices are equal")
    else:
        print("Matrices aren't equal")