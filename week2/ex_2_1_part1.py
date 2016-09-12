#!/usr/bin/python
import sys


filename = sys.argv[1]


def table_to_list_of_lists(filename):
    with open(filename, 'r') as f:
        data = f.read().splitlines()

    big_list = []
    small_list = []

    for line in data:
        for number in line.split():
            small_list.append(int(number))
        big_list.append(small_list)
        small_list = []

    return big_list

sys.stdout.write("%s" % table_to_list_of_lists(filename))

