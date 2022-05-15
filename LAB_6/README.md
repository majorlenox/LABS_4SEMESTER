LAB_6: Strassen algorithm
-
The program multiplies matrices: 
1. Trivial 
2. Using the Strassen algorithm 
3. Using the Strassen algorithm on multiple cores

And compares the time of each method.

Description of modules:
-
- main.py - Accepts the path to the file with the matrices (-f filename [default = "./matrices.txt"]) or generates them depending on the passed parameters of the size of the matrices (-n -mn -m).
- matrix.py - Contains the main ways of interacting with matrices. Also, the parameters of their generation: RAND_DIGITS = 2 (number of digits after the decimal point), RAND_RANGE = 100 (maximum number generated). 


Usage:
-
 - main.py - 


test: 
- 
- preimage =  b'\x1A\xC1\x00\x00\x03\x00\x00\x00'
- image    = 83307d0603279add28aa4c9b5debeca8

> $ python3 main.py 83307d0603279add28aa4c9b5debeca8
>
> preimage founded: b'\x1a\xc1\x00\x00\x03\x00\x00\x00'
> 
> Time: 3.846397351 seconds

- preimage =  b'\x06\x11\x00\x00\x04\x00\x00\x00'
- image    = 87b223887eaac384c3850f7e7c9d16f5

> $ python3 main.py 87b223887eaac384c3850f7e7c9d16f5
>
> preimage founded: b'\x06\x11\x00\x00\x04\x00\x00\x00'
> 
> Time: 0.343149338 seconds



- Resources:
  - https://en.wikipedia.org/wiki/Strassen_algorithm
  - https://matrixcalc.org
  - 