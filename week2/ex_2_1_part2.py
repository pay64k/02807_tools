#!/usr/bin/python
import sys

_input = sys.stdin.readline()
_save_to_name = sys.argv[1]


def lists_of_lists_to_table(input_str, save_to_name):

    # inspired by: http://stackoverflow.com/questions/2644221/how-can-i-convert-this-string-to-list-of-lists
    strs = input_str.replace('[', '').replace(' ','').split('],')
    list_of_lists = [s.replace(']', '').split(',') for s in strs]
    # ---

    big_table = ''
    row_in_table = ""

    for _list in list_of_lists:
        for number in _list:
            row_in_table = row_in_table + number + " "
        big_table = big_table + row_in_table + "\n"
        row_in_table = ""

    with open(save_to_name, 'w') as file_:
        file_.write(big_table)

    return "ok"

lists_of_lists_to_table(_input, _save_to_name)
