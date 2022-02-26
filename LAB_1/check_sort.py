def from_sha1_to_numbers(sha1_array):
    numbers = []  # every 16 hex (64 bits) becomes one decimal number (from 0 to 2^64 - 1)
    for sha1 in sha1_array:
        numbers.append(int(sha1[0:16], 16))
    return numbers


f1 = f2 = f3 = f4 = True

with open("SHA1_sorted_qsGreater.txt") as file:
    input = file.read().split('\n')
    for i in range(3):
        input.pop(len(input) - 1)
    numbers = from_sha1_to_numbers(input)
    for i in range(len(numbers) - 1):
        if numbers[i] > numbers[i+1]:
            f1 = False
            break

with open("SHA1_sorted_qsLess.txt") as file:
    input = file.read().split('\n')
    for i in range(3):
        input.pop(len(input) - 1)
    numbers = from_sha1_to_numbers(input)
    for i in range(len(numbers) - 1):
        if numbers[i] < numbers[i + 1]:
            f2 = False
            break

with open("SHA1_sorted_msGreater.txt") as file:
    input = file.read().split('\n')
    for i in range(3):
        input.pop(len(input) - 1)
    numbers = from_sha1_to_numbers(input)
    for i in range(len(numbers) - 1):
        if numbers[i] > numbers[i + 1]:
            f3 = False
            break

with open("SHA1_sorted_msLess.txt") as file:
    input = file.read().split('\n')
    for i in range(3):
        input.pop(len(input) - 1)
    numbers = from_sha1_to_numbers(input)
    for i in range(len(numbers) - 1):
        if numbers[i] < numbers[i + 1]:
            f4 = False
            break

if f1:
    print("qsGreater works correctly.")
else:
    print("qsGreater has some errors!")

if f2:
    print("qsLess works correctly.")
else:
    print("qsLess has some errors!")

if f3:
    print("msGreater works correctly.")
else:
    print("msGreater has some errors!")

if f4:
    print("msLess works correctly.")
else:
    print("msLess has some errors!")
