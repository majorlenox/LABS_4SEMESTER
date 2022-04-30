LAB_5: MD4 hash and "meeting in the middle"
-
The program implements a search for the preimage by its hash(MD4), taking into account the features of the preimage
(it is <= 8 bytes), which makes it possible to reduce the duration of the check due to the "meeting in the middle".

Usage:
-
 - main.py - Accepts a hash(MD4) and searches for a prototype using it
 - hash.py - You can use it to generate a hash(MD4), (only manually!)


test: 
- 
- preimage =  b'\x1A\xC1\x00\x00\x03\x00\x00\x00'
- image    = 83307d0603279add28aa4c9b5debeca8

> $ python3 main.py 83307d0603279add28aa4c9b5debeca8
>
> preimage founded: b'\x1a\xc1\x00\x00\x03\x00\x00\x00'
> 
> Time: 3.846397351 seconds

- Resources:
  - https://github.com/hashcat/hashcat/blob/master/OpenCL/m01000_a3-optimized.cl
  - https://ru.wikipedia.org/wiki/MD4
  - https://gist.github.com/kangtastic/c3349fc4f9d659ee362b12d7d8c639b6
  