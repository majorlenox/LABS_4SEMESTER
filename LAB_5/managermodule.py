from multiprocessing import Process

NUMBER_OF_PROCESSES = 4

def inner_loop(x1):
    for x0 in range(4294967296):
        #

def work(input_md4):
    processes = []
    # outer loop
    for x1 in range(4294967296):
        x1b = bin(x1).removeprefix('0b')
        x1b = '0'*(32 - len(x1b)) + x1b
        proc = Process(target=inner_loop, args=tuple([list(x1b)]))
        processes.append(proc)
        proc.start()
        if x1 % NUMBER_OF_PROCESSES == NUMBER_OF_PROCESSES - 1:
            for proc in processes:
                proc.join()