# -*- coding: utf-8 -*-
'''
=====
ABOUT
=====

Solution for the Advent of Coding 2023, day 15 challenge.
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
import re


# Type the path to your input text file here if you do not wish to use the command line argument
FILENAME = "./inputs/day15.txt"


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
    Function loads the contents of the given text file and returns the contents as a string.
    @param fn:      path to the file to-be-loaded
    @returns:       contents of the file as a string
    '''
    with open(fn,'r') as file:
        ret = ''
        for line in file:   # Loop through the file and add the lines to the return value
            ret += line
    return ret

# =========================


def holiday_ascii_string_helper(inp):
    '''
    Hashes the input as per the assignment
    '''
    ret = 0
    for char in inp:
        ret = (ret + ord(char))*17 % 256
    return ret



# =========================

def part1(data: list) -> int:
    '''
    Solution for the part 1.
    '''
    ans = 0
    for section in data.split(','):
        section = section.strip()
        if not section:
            continue
        ans += holiday_ascii_string_helper(section)

    return ans


def part2(data: list) -> int:
    '''
    Solution for the part 2.
    '''
    # List of all the 256 boxes, in the correct order. Each of these 256 entries is a list containing the labels of the
    # lenses inside, in the correct order (first lens on first position and so on)
    boxes   = [[] for i in range(256)]

    # Dictionary keeping track of each lense's focal length. Note that as the box is determined by the lens label's hash value,
    # a lens with a certain name cannot exist in multiple boxes -> there are no risk of having a similarly labeled lens in multiple boxes
    lenses  = {}

    for section in data.split(','):

        # If command is -: remove the lens from the corresponding box, if it exists there
        if '-' in section:
            lens_label  = section.split('-')[0]
            box_id      = holiday_ascii_string_helper(lens_label)
            if lens_label in boxes[box_id]:
                boxes[box_id].remove(lens_label)

        # If command is =: add the lens to the corresponding box, _if it already isn't there_ (if it does, no modifications to the position),
        # and update the lense's focal length
        if  '=' in section:
            lens_label      = section.split('=')[0]
            focal_length    = int(section.split('=')[1])
            box_id          = holiday_ascii_string_helper(lens_label)
            lenses[lens_label] = focal_length
            if lens_label not in boxes[box_id]:
                boxes[box_id].append(lens_label)

    # Go through each lens in each box and calculate the total focusing  power as per the assignment
    total_focusing_power = 0
    for box_id, box in enumerate(boxes, start=1):
        for lens_slot, lens_id in enumerate(box, start=1):
            total_focusing_power += box_id * lens_slot * lenses[lens_id]

    return total_focusing_power

# =========================

if  __name__ == "__main__":
    fn = get_fn()
    data = load_file(fn)

    print(f"Part 1 solution: {part1(data)}")
    print(f"Part 2 solution: {part2(data)}")
