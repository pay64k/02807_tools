#!/usr/bin/python
import numpy as np
import sys
from numpy.linalg import solve


bla = [
    [1,2,3,4],
    [6,9,12,7],
    [2,0,9,10]
]

filename = sys.argv[1]

with open(filename, 'r') as f:
    data = f.read().splitlines()

# print data
#
# big = [map(int, x) for line in data for x in line.split(',')]
#
# print big

big = []
small = []
for line in data:
    for num in line.split(','):
        small.append(int(num))
    big.append(small)
    small = []

A = np.array(big)[0:3,0:3]
b = np.array(big)[:,3:4]


print solve(A,b)