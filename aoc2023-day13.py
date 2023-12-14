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
FILENAME = "./inputs/day13.txt"


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
    return ret.split('\n\n')

# =========================

def transpose_map(map: list)  -> list:
    '''
    Transposes the given map: first row becomes first column, second row becomes the second column, and so on.
    The map is assumed to have strings as its entries rather than lists, so it is actually a 1D-list.
    Example:
        map = ['1234','5678']
        returns ['15','26','37','48']
    '''
    # Transform the rows from strings to lists of strings
    map_transposed = [[char for char in row] for row in map]

    # Tranpose the map
    map_transposed = [list(col) for col in zip(*map_transposed)]

    # Rows to strings
    map_transposed = [''.join(row) for row in map_transposed]
    return map_transposed


def find_horizontal_mirrors(map: list) -> int:
    '''
    Finds horizontal mirrors, i.e. mirrors across multiple columns.
    Returns the number of rows before the first mirror (that is, index_of_row_before_the_mirror + 1),
    function does not check if there would be other mirrors as well.
    Returns 0 if no horizontal reflections could be found.
    '''
    def _horizontal_mirror_recursion(map: list, row_idx_1: int, row_idx_2:int) -> bool:
        '''
        Checks if two rows are exactly the same. If they are, recursively check the similarity of the row before the first
        and the row after the second row.
        Returns True if the map could be mirrored the whole way, False if not.
        '''
        # If one index is outside the map, the mirroring was successful
        if row_idx_1 < 0 or row_idx_2 >= len(map):
            return True
        # If the two rows are the same, recursively check the rows before firstrow and after second row
        if map[row_idx_1] == map[row_idx_2]:
            return _horizontal_mirror_recursion(map, row_idx_1-1, row_idx_2+1)
        # If there were differences, mirroring could not be done
        return False
    
    # Check through each pair of adjacent rows if the map could be mirrored between those rows
    for first_row_idx in range(len(map)):
        is_mirrored = _horizontal_mirror_recursion(map, first_row_idx, first_row_idx+1)
        if is_mirrored:
            return first_row_idx + 1
    
    # If no mirrors could be found, return 0
    return 0


def find_horizontal_mirrors_with_smudge(map: list) -> int:
    '''
    Finds horizontal mirrors, i.e. mirrors across multiple columns, with exactly one smudge
    (i.e. exactly one "error" in the reflection).
    Returns the number of rows before the first mirror (that is, index_of_row_before_the_mirror + 1),
    function does not check if there would be other mirrors as well.
    Returns 0 if no horizontal reflections could be found.
    '''
    def _nof_differences(s1: str, s2: str) -> int:
        '''
        Returns the number of (positional) differences between two strings.
        For example, s1='..#.#', s2='#...#', returns 2
        '''
        return len([1 for c1, c2 in zip(s1,s2) if c1 != c2])

    def _horizontal_mirror_recursion(map: list, row_idx_1: int, row_idx_2: int, smudge_corrected: bool) -> bool:
        '''
        Checks if two rows are exactly the same. If they are, recursively check the similarity of the row before the first
        and the row after the second row.
        Exactly one error is _required_ across all the reflections, this is depicted in the boolean smudge_corrected.
        If an error is found, flip the boolean to True and continue; terminate the search for the second error encountered.
        Returns True if the map could be mirrored the whole way (with exactly one error), False if not.
        '''
        # Outside the map -> recursion is complete. As exactly one error is required, return the info is such an error was met or not
        if row_idx_1 < 0 or row_idx_2 >= len(map):
            return smudge_corrected
        # Check the number of differences between the rows. If none, continue recursion and do not switch the smudge_corrected flag.
        # If exactly one difference, if a difference was not met previously, continue recursion but set the flag smudge_corrected to True.
        # If exactly one difference and a difference was met previously, or multiple differences, failure -> abort search and return False.
        nof_differences = _nof_differences(map[row_idx_1], map[row_idx_2])
        if nof_differences == 0:
            return _horizontal_mirror_recursion(map, row_idx_1-1, row_idx_2+1, smudge_corrected)
        elif nof_differences == 1 and not smudge_corrected:
            return _horizontal_mirror_recursion(map, row_idx_1-1, row_idx_2+1, True)
        return False
    
    # Check through each pair of adjacent rows if the map could be mirrored between those rows
    for first_row_idx in range(len(map)):
        is_mirrored = _horizontal_mirror_recursion(map, first_row_idx, first_row_idx+1, False)
        if is_mirrored:
            return first_row_idx + 1
        
    # If no mirrors could be found, return 0
    return 0


def part1(data: list) -> int:
    '''
    Solution for the part 1.
    '''
    summarize = 0
    for part in data:
        map = part.split("\n")

        # Horizontal mirrors
        summarize += 100 * find_horizontal_mirrors(map)

        # Vertical mirrors -> transpose the map and then look for horizontal mirrors
        map_t = transpose_map(map)
        summarize += find_horizontal_mirrors(map_t)

    return summarize


def part2(data: list) -> int:
    '''
    Solution for the part 2.
    '''
    summarize = 0
    for part in data:
        map = part.split("\n")

        # Horizontal mirrors
        summarize += 100 * find_horizontal_mirrors_with_smudge(map)

        # Vertical mirrors -> transpose the map and then look for horizontal mirrors
        map_t = transpose_map(map)
        summarize += find_horizontal_mirrors_with_smudge(map_t)

    return summarize


# =========================

if  __name__ == "__main__":
    fn = get_fn()
    data = load_file(fn)

    print(f"Part 1 solution: {part1(data)}")
    print(f"Part 2 solution: {part2(data)}")