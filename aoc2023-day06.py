# -*- coding: utf-8 -*-
'''
=====
ABOUT
=====

Solution for the Advent of Coding 2023, day 6 challenge.
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
FILENAME = "./inputs/day06.txt"


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


def parse_games_task1(data):
    '''
    Function parses the input data into games.
    Returns a list in the form of [[time1,distance1],[time2,distance2], ...]
    '''
    times       = [int(val.strip()) for val in data[0].split(" ")[1:] if val]
    distances   = [int(val.strip()) for val in data[1].split(" ")[1:] if val]
    games       = [[time,  distance] for time, distance in zip(times, distances)]
    return games

def parse_games_task2(data):
    '''
    Function parses the input data into one long game.
    Returns a list in the form of [time, distance].
    '''
    time       = int(''.join([val.strip() for val in data[0].split(":")[1].strip().split(" ")]))
    distance   = int(''.join([val.strip() for val in data[1].split(":")[1].strip().split(" ")]))
    return [time, distance]

def solve_quadratic_equation(a,b,c):
    '''
    Solves an equation of form ax^2 + bx + c = 0.
    '''
    if b**2 - 4*a*c < 0:
        return None
    roots = [(-b - math.sqrt(b**2 - 4*a*c))/(2*a), (-b + math.sqrt(b**2 - 4*a*c))/(2*a)]
    roots.sort()
    return roots

def ways_to_beat_record(t_total, record):
    '''
    Determines the number of ways to beat the record, as explained in the assignment, exploiting the fact that the
    distance traveled is a cubical function of the time pressed:
        d_traveled = -t_press^2 + t_total*t_press
    When written in the form
        victory = -t_press^2 + t_total*t_press - record
    the variable 'victory' is positive when the resulting distance is larger than the record, and the number
    of ways to win the record can then be determined by calculating the roots of the equation.
    '''
    low_root, high_root = solve_quadratic_equation(a=-1, b=t_total, c=-record)
    return math.floor(high_root) - math.ceil(low_root) + 1

def task1(games):
    '''
    Solution for task 1.
    '''
    prod = 1
    for t_total, record in games:
        prod = prod * ways_to_beat_record(t_total, record)
    return prod

def task2(game):
    '''
    Solution for task 2.
    '''
    t_total, record = game
    return ways_to_beat_record(t_total, record)


# =========================

if  __name__ == "__main__":
    fn = get_fn()
    data = load_file(fn)

    # Task 1
    games1 = parse_games_task1(data)
    print(f"Task 1 solution: {task1(games1)}")

    # Task 2
    games2 = parse_games_task2(data)
    print(f"Task 2 solution: {task2(games2)}")