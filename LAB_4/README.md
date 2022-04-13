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
  - -ts - Text size, file size text.txt in Bytes. Default=1024
  - -f  - Frequency of occurrence of lines from substrings.txt in text.txt. Default=5
  
Resources:
- Bloom filter, mmh3
  - https://en.wikipedia.org/wiki/Bloom_filter
  - https://github.com/Lexcorp3439/bloom-filter
  - https://progi.pro/generirovanie-k-parno-nezavisimih-hesh-funkciy-3706183