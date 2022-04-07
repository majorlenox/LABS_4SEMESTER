LAB_4: Python 3.9, Substring search using Bloom filter and Rabin–Karp algorithm
=

generator.py
-

Generates the following files:


- substrings.txt:
  - Stores a set of a string of a given length. Characters are: A-Z, a-z, punctuation.

- text.txt:
  - A file of a given size with a given frequency of occurrence of lines from the file substrings.txt
  

- Usage:
  - $ python3 generator.py -sn 10 -ss 5 -ts 5 -f 10


- flags: 
  - -sn - Number of Substrings, how many lines would be in substrings.txt. Default=20  
  - -ss - Substring Size, how many characters will be in each line. Default=10
  - -ts - Text size, file size text.txt in kB. Default=10
  - -f  - Frequency of occurrence of lines from substrings.txt in text.txt. Default=5


main.py:
-
Factorizes a number specified in decimal or hexadecimal notation

- Usage: 
  - $ python3 main.py -d 2701
  - output: 37, 73
  

- flags: 
  - -d - The number for factorization is entered in decimal form  
  - -x - The number for factorization is entered in hexadecimal form
  - -o - The number for factorization is entered in octal form


- Output: 
  - the sequence of prime factors


Resources:
- https://codesigningstore.com/what-is-the-best-hashing-algorithm
- 