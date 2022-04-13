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
  - -sn - Number of Substrings, how many lines would be in substrings.txt. Default=10  
  - -ss - Substring Size, how many characters will be in each line. Default=10
  - -ts - Text size, file size text.txt in KBytes. Default=1
  - -f  - Frequency of occurrence of lines from substrings.txt in text.txt. Default=5
  
main.py
-

Starts the managermodule.py, which accepts input substring.txt and text.txt, creates a bloom filter
and searches for lines from the file substring.txt using parallelization:

- Usage:
  - $ python3 main.py -m 1000 substring.txt text.txt -f


- flags: 
  - -f         - Output the offset of only the first occurrence. Default=0
  - -ss        - Filter Bloom size in Bytes. Default=2000
  - substrings - Path to file with substrings. 
  - text       - Path to file with text.
  

test
-
Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz

65 number of substrings
75 size of each substring
2 MB text
5% frequency
2 KB Bloom Filter

$ python3 generator.py -sn 65 -ss 75 -ts 2048 -f 5
Time: 5.790046151 seconds
- files: test1subs.txt, test1text.txt 

$ python3 main.py test1subs.txt, test1text.txt
Time: 113.203555383 seconds


Resources:
- Bloom filter, mmh3
  - https://en.wikipedia.org/wiki/Bloom_filter
  - https://github.com/Lexcorp3439/bloom-filter
  - https://progi.pro/generirovanie-k-parno-nezavisimih-hesh-funkciy-3706183