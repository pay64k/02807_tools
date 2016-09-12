#!/usr/bin/python
import sys
number = int(sys.argv[1])

max_amount = 2**number

print "max: ", max_amount


def dec_to_bin(x):
    if x == 0: return [0]
    bit_pattern = []
    while x:
        bit_pattern.append(x % 2)
        x /= 2
    return bit_pattern[::-1]

bits = [dec_to_bin(num) for num in range(0,max_amount,1)]

for pattern in bits:
    if len(pattern) < number:
        missing_zeros = number - len(pattern)
        while missing_zeros:
            pattern.insert(0,0)
            missing_zeros -= 1

# print bits
for line in bits:
    print line
