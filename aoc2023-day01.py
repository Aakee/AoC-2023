# -*- coding: utf-8 -*-
'''
=====
ABOUT
=====

Solution for the Advent of Coding 2023, day 1 challenge.
More information from the official website: https://adventofcode.com/2023


==========
HOW TO RUN
==========

You can run the script by calling
    [path-to-python-intepreter] [path-to-this-script] [path-to-input-text-file]
For example:
    python ./aoc2023-day01.py ./inputs/day01.txt

Alternatively, you can modify the FILENAME constant at the beginning of the script to give the path to the input file.
If both command line argument and hard-coded filename is given, the command line argument takes precedence.


======
GIT REPOSITORY
======
The git repository for my solutions for AoC 2023 challenges can be found here: https://github.com/Aakee/AoC-2023


======
AUTHOR
======

Akseli Konttas, December 2023

'''
import argparse
import collections
import itertools
import math


# Type the path to your input text file here if you do not wish to use the command line argument
FILENAME = "./inputs/day01.txt"


def get_fn() ->  str:
    '''
    Function extracts the input file from thecommandline argument, if given.
    Based on whether the argument was given or not, the function returns the given name, or the hard-coded name on
    the constant FILENAME.
    @returns:       the input file path/name, if given on command line;
                    or FILENAME, if not given on command line
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('input_fn', nargs='?', default=FILENAME, help="Path to the input text file. Optional; if not given, will default to the one hard-coded in the beginning of the script file.")
    args =  parser.parse_args()
    return args.input_fn


def load_file(fn: str)  -> str:
    '''
    Function loads the contents of the given text file and returns the contents as a list, with the file splitted from line breaks.
    @param fn:      path to the file to-be-loaded
    @returns:       contents of the file as a string
    '''
    with open(fn,'r') as file:
        ret = ''
        for line in file:   # Loop through the file and add the lines to the return value
            ret += line
    return ret.split('\n')

# =========================

def find_first_digit_in_string(string):
    '''
    Function finds and returns the first digit (0-9) it finds in a string, or None if none found.
    '''
    num = None
    for char in string:
        try:
            num = int(char)
            break
        except ValueError:
            continue
    return num

def find_last_digit_in_string(string):
    '''
    Function finds and returns the last digit (0-9) it finds in a string, or None if none found.
    '''
    reversed = string[::-1]
    return find_first_digit_in_string(reversed)

def find_spelled_out_number(string):
    '''
    Function finds and returns an out-spelled number ('one', 'two'...) in the given string.
    If there are multiple, the function returns the largest of those numbers.
    '''
    num = None
    if "one" in string:
        num = 1
    if "two" in string:
        num = 2
    if "three" in string:
        num = 3
    if "four" in string:
        num = 4
    if "five" in string:
        num = 5
    if "six" in string:
        num = 6
    if "seven" in string:
        num = 7
    if "eight" in string:
        num = 8
    if "nine" in string:
        num = 9
    return num

def find_first_number(line):
    '''
    Finds and returns the first number of the given line, be it a digit or an out-spelled number.
    '''
    # Idea: Take first only the first character and see if it either contains a digit or an out-spelled digit.
    # If not, take first two characters as a substring and conduct the search again, then three and so on, until a value is found.
    num = None
    for idx in range(len(line)+1):
        substr = line[:idx]
        num = find_spelled_out_number(substr)
        if num is not None:
            break
        num = find_first_digit_in_string(substr)
        if num is not None:
            break
    return num

def find_last_number(line):
    '''
    Finds and returns the last number of the line, be it a digit of out-spelled number.
    '''
    # Idea: Take first only the last character and see if it either contains a digit or an out-spelled digit.
    # If not, take last two characters as a substring and conduct the search again, then three and so on, until a value is found.
    num = None
    for idx in range(len(line),-1,-1):
        substr = line[idx:]
        num = find_spelled_out_number(substr)
        if num is not None:
            break
        num = find_last_digit_in_string(substr)
        if num is not None:
            break
    return num

def task1(data):
    '''
    Finds and returns the answer for the first task.
    '''
    calibvalue = 0
    for idx, line in enumerate(data):
        first = find_first_digit_in_string(line)
        last  = find_last_digit_in_string(line)
        if first is not None and last is not None:
            calibvalue += 10*first + last
        else:
            print(f"Error with line {idx}: line={line}, first={first}, last={last}")
    return calibvalue

def task2(data):
    '''
    Finds and returns the answer for the second task.
    '''
    calibvalue = 0
    for idx, line in enumerate(data):
        first = find_first_number(line)
        last  = find_last_number(line)
        if first is not None and last is not None:
            calibvalue += 10*first + last
        else:
            print(f"Error with line {idx}: line={line}, first={first}, last={last}")
    return calibvalue

# =========================

if  __name__ == "__main__":
    fn = get_fn()
    data = load_file(fn)

    # First task
    print(f"First task: {task1(data=data)}")

    # Second task
    print(f"Second task: {task2(data=data)}")