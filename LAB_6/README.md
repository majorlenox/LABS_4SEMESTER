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
- strassen.py - Contains the TRIVIAL_MULTIPLICATION_BOUND parameter, which is responsible for using trivial multiplication instead of strassen for smaller n, a NUMBER_OF_PROCESS - for multiprocessing. And contains:
three implementations of multiplying matrices:
  - with list matrices
  - with np matrices (faster than a list by about 20%)
  - multiprocess with np matrices (fastest)
  

Usage:
-
 - main.py - 


test: 
- 

TRIVIAL_MULTIPLICATION_BOUND = 128
1000 - 332.80 seconds trivial
     - 194.14 seconds strassen

TRIVIAL_MULTIPLICATION_BOUND = 64
1000 - 333.62 seconds trivial
     - 171.68 seconds strassen

TRIVIAL_MULTIPLICATION_BOUND = 32
1000 - 333.10 seconds trivial
     - 160.52 seconds strassen

TRIVIAL_MULTIPLICATION_BOUND = 16
1000 - 338.11 seconds trivial
     - 167.54 seconds strassen


- Resources:
  - https://en.wikipedia.org/wiki/Strassen_algorithm
  - https://matrixcalc.org
  - https://cristianbastidas.com/my-blog/en/algorithms/python/tutorial/wiki/2021/10/13/strassen.html