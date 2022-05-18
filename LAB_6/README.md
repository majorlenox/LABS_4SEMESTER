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
- strassen.py - Contains the TRIVIAL_MULTIPLICATION_BOUND parameter, which is responsible for using trivial multiplication instead of strassen for smaller n. And contains:
three implementations of multiplying matrices:
  - with list matrices
  - with np matrices (faster than a list by about 20%)
  - multiprocess with np matrices (fastest)
  

Usage:
-
 - main.py - 
"python3 main.py -n 50 -mn 44 -m 23" - generate and multiply 50x44 and 44x23 matrices 
"python3 main.py -f" - Load matrices from file ./matrices.txt and multiply them
"python3 main.py -f sample.txt" - Load matrices from file ./sample.txt and multiply them

options: 
- -s - save generated matrices
- -d - display them to stdout

test: 
- 
for 1000 elements, trivial's time are about 325 seconds
| TRIVIAL_MULTIPLICATION_BOUND | strassen's time (s) |  
| ---------------------------- | ------------------- |
|                          128 |              188.14 |
|                           64 |              167.68 |
|                           32 |              149.27 |
|                           16 |              162.54 |

Testing for TRIVIAL_MULTIPLICATION_BOUND = 32:
| Elements | trivial's time (s) | strassen's time (s) | strassen's multiprocess time (s) |  
| -------- | -----------------  | ------------------- | -------------------------------- | 
|      150 |              0.99  |                3.07 |                            0.70  |
|      300 |              8.73  |               21.57 |                            4.67  | 
|     1000 |               322  |               149.9 |                            34.13 |
|     1500 |                NaN |                 NaN |                           257.51 |



- Resources:
  - https://en.wikipedia.org/wiki/Strassen_algorithm
  - https://matrixcalc.org
  - https://cristianbastidas.com/my-blog/en/algorithms/python/tutorial/wiki/2021/10/13/strassen.html