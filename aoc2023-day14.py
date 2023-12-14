# -*- coding: utf-8 -*-
'''
=====
ABOUT
=====

Solution for the Advent of Coding 2023, day 14 challenge.
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
FILENAME = "./inputs/day14.txt"


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
    return ret.split('\n')

# =========================

def rotate_map_clockwise(map):
    '''
    Function takes a 2D-list as an input and creates a copy, which is rotated 90 degrees clockwise.
    For example:
        rotate_map_clockwise(  [[1,2,3],
                                [4,5,6],
                                [7,8,9]])

        returns                [[7,4,1],
                                [8,5,2],
                                [9,6,3]]
    '''
    return [list(column[::-1]) for column in zip(*map)]


def tilt_to_north(map: list):
    '''
    Tilts the map to north: moves all round stones (O) as far nort as they can. They can go over empty
    spaces (.), but not over rectangular stones (#) or each other.
    Returns the tilted map, though the operations are done on the original input map.
    '''
    # Dictionary to keep tracks which spots (rows) on each column are empty
    # -> to which spaces the stones can roll to
    available_spots = {}
    for col_idx in range(len(map[0])):
        available_spots[col_idx] = []

    # Loop through each row, and on each row loop through each column
    for row_idx in range(len(map)):
        for col_idx in range(len(map[row_idx])):

            # Current space has a round boulder: check if there are empty spaces to north where this boulder can roll to
            if map[row_idx][col_idx] == 'O':
                empty_rows = available_spots[col_idx]

                # If there are: move the boulder to the first (northernmost) empty space, set this space as empty, and remove the previously empty space from the list
                if len(empty_rows) > 0:
                    map[empty_rows[0]][col_idx] = 'O'
                    map[row_idx][col_idx] = '.'
                    available_spots[col_idx].pop(0)

            # Current space is empty: add the space to the list of empty spaces
            # (this can be a space where a boulder was moved away just in previous if clause!)
            if map[row_idx][col_idx] == '.':
                available_spots[col_idx].append(row_idx)

            # Current space has a rectangular space: empty the list of empty spaces, as no boulders can roll past this boulder
            if map[row_idx][col_idx] == '#':
                available_spots[col_idx] = []

    return map


def calculate_load(map):
    '''
    Function calculates and returns the load to the north support beams as per the assignment.
    '''
    ans = 0
    for coeff, row in enumerate(map[::-1], start=1): # Enumerate from bottom to up, starting from index 1
        ans += coeff * len([stone for stone in row if stone == 'O'])
    return ans


# =========================

def part1(map: list) -> int:
    '''
    Solution for the part 1.
    '''
    map = [[obj for obj in row] for row in map if row.strip()] # Transform the rows from strings to lists of strings, e.g. '.#.O.' -> ['.', '#', '.', 'O', '.']
    map = tilt_to_north(map)
    return calculate_load(map)


def part2(map: list) -> int:
    '''
    Solution for the part 2.
    '''
    map = [[obj for obj in row] for row in map if row.strip()] # Transform the rows from strings to lists of strings, e.g. '.#.O.' -> ['.', '#', '.', 'O', '.']
    states_encountered  = {}    # Dictionary to keep track on which map states has already been encountered, and on which cycle numbers
    weights             = {}    # Dictionary to record information on all cycles' load weights
    target_cycle        = 1_000_000_000   # From the assignment

    for cycle in range(1,target_cycle+1):
        # Idea: Tilting north->west->south->east is equivalent to tilting north, then rotating the whole map 90 degrees clockwise, then
        # tilting north again, then rotating again, and so on, altogether four times each. This avoids the need of writing multiple functions for
        # tilting the map

        # North
        map = tilt_to_north(map)

        # West
        map = rotate_map_clockwise(map)
        map = tilt_to_north(map)

        # South
        map = rotate_map_clockwise(map)
        map = tilt_to_north(map)

        # East
        map = rotate_map_clockwise(map)
        map = tilt_to_north(map)

        # Rotate back to north
        map = rotate_map_clockwise(map)
        
        # Check if the resulting map state has been encountered
        map_as_str = ''.join([''.join(row) for row in map])
        if map_as_str in states_encountered:

            # As we have been in this state before, there is no need to continue rotating, as from now on the behaviour will be periodic
            # Extract the load of the target cycle count from the past load values
            previous_cycle  = states_encountered[map_as_str]                    # Previous cycle number where this exact state was encountered
            period_length   = cycle - previous_cycle                            # Period length: this count number - count number when last this state appeared
            rem             = (target_cycle-previous_cycle) % period_length     # After haw many cycles of this one will be the same load value as the target count

            return weights[previous_cycle+rem]

        # If for some reason we hit the target count, just return the load value of this cycle
        if cycle == target_cycle:
            return calculate_load(map)

        # Save this map state and load value
        states_encountered[map_as_str]  = cycle
        weights[cycle]                  = calculate_load(map)


# =========================

if  __name__ == "__main__":
    fn = get_fn()
    data = load_file(fn)

    print(f"Part 1 solution: {part1(data)}")
    print(f"Part 2 solution: {part2(data)}")