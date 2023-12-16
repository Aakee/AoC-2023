# -*- coding: utf-8 -*-
'''
=====
ABOUT
=====

Solution for the Advent of Coding 2023, day 16 challenge.
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
import queue


# Type the path to your input text file here if you do not wish to use the command line argument
FILENAME = "./inputs/day16.txt"


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
    return [[obj for obj in row] for row in ret.split('\n')]

# =========================

# Coordinates for the different compass coordinates
DIRECTIONS =   { "N": {'row': -1, 'col':  0},
                 "S": {'row':  1, 'col':  0},
                 "W": {'row':  0, 'col': -1},
                 "E": {'row':  0, 'col':  1},                       
                }


def reflect_light(direction, mirror):
    '''
    Reflects the light going to direction 'direction' hitting a mirror shaped 'mirror'.
    Returns the direction where the light continues after reflecting from this mirror.
    '''
    if mirror == '/':
        ref = {'N':'E' ,'E':'N', 'S':'W', 'W':'S'}
        return ref[direction]
    if mirror == '\\':
        ref = {'N':'W' ,'W':'N', 'S':'E', 'E':'S'}
        return ref[direction]
    

def split_light(direction, splitter):
    '''
    Splits the light going to direction 'direction' hitting a splitter shaped 'splitter'.
    Returns the directions where the light continues after being splitted from this splitter, as a list.
    Note that depending on the initial direction and the splitter type, the returned list can contain either one or two directions.
    '''
    split_directions = []
    if splitter == '|' and direction in ('W','E'):
        split_directions.append('N')
        split_directions.append('S')
    elif splitter == '-' and direction in ('N','S'):
        split_directions.append('W')
        split_directions.append('E')
    else:
        split_directions.append(direction)
    return split_directions


def n_energized_tiles(maze, row, col, direction):
    '''
    Calculates and returns the number of energized tiles, when the light enters the 'maze' from coordinates ['row', 'column'] going to direction 'direction'.
    '''
    status  = [[list() for col in row] for row in data]     # 2D-list same size as maze containing information of to which directions a light beam has already passed through any tile
    q       = queue.Queue()                                 # Queue holding info of paths not yet traversed
    stop    = False                                         # Flag telling if all paths have been traversed

    while not stop:
        status[row][col].append(direction)
        current_tile = maze[row][col]

        # Current tile is mirror: next tile is rotated to some direction
        if current_tile in ('/', '\\'):
            direction = reflect_light(direction, current_tile)

        # Current tile is splitter: either continues in straight line or splits into two beams.
        # The logic to determine this is in split_light
        elif current_tile in ('-','|'):
            next_directions = split_light(direction, current_tile)
            direction = next_directions[0]
            if len(next_directions) > 1:    # If there are multiple, splits light -> put the additional into queue to process it later
                q.put([row, col, next_directions[1]])
        else:
            direction = direction

        # Next tile, according to the determined direction
        row = row + DIRECTIONS[direction]['row']
        col = col + DIRECTIONS[direction]['col']

        # If the tile is outside the maze or it has already been processed, terminate and take next from queue
        while not 0 <= row < len(maze) or not 0 <= col < len(maze[0]) or direction in status[row][col]:
            if q.empty():
                stop = True
                break
            row, col, direction = q.get()
            row = row + DIRECTIONS[direction]['row']
            col = col + DIRECTIONS[direction]['col']

    # 2D to 1D
    status_flattened    = [obj for row in status for obj in row]
    n_energized         = len([lst for lst in status_flattened if len(lst) > 0])
    return n_energized


# =========================

def part1(maze: list) -> int:
    '''
    Solution for the part 1.
    '''
    n_energized = n_energized_tiles(maze, 0, 0, 'E')
    return n_energized


def part2(maze: list) -> int:
    '''
    Solution for the part 2.
    '''
    max_energized = 0
    max_row = len(maze)-1
    max_col = len(maze[0])-1

    for row in range(max_row+1):
        max_energized = max(max_energized, n_energized_tiles(maze,  row,        0,  'E'))
        max_energized = max(max_energized, n_energized_tiles(maze,  row,  max_col,  'W'))

    for col in range(max_col+1):
        max_energized = max(max_energized, n_energized_tiles(maze,        0,  col,  'S'))
        max_energized = max(max_energized, n_energized_tiles(maze,  max_row,  col,  'N'))

    return max_energized

# =========================

if  __name__ == "__main__":
    fn = get_fn()
    data = load_file(fn)

    print(f"Part 1 solution: {part1(data)}")
    print(f"Part 2 solution: {part2(data)}")