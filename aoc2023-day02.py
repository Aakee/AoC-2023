# -*- coding: utf-8 -*-
'''
=====
ABOUT
=====

Solution for the Advent of Coding 2023, day 2 challenge.
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
FILENAME = "./inputs/day02.txt"


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


def is_game_legal(line):
    '''
    Function checks if a given game is legal according to the game 1 rules,
    i.e. all the runs had a certain maximum of differently colored squares.
    @param line: One line from the input file. Has a format of
        "Game 0: 1 red, 3 green, 5 blue; 2 red, 8 green, 7 blue"
    @returns: True if game is legal, False if not
    '''
    # From assignment
    max_values = {  'red':   12,
                    'green': 13,
                    'blue':  14}
    
    game_header, game_data = line.split(":") # First split: ["Game 0", "1 red, 3 green, 5 blue; 2 red, 8 green, 7 blue"]
    game_id = int(game_header.split(" ")[1]) 
     
    runs = game_data.split(";")             # ["1 red, 3 green, 5 blue", "2 red, 8 green, 7 blue"]
    for run in runs:
        colors = run.split(",")              # ["1 red", "3 green", "5 blue"]
        for color in colors:
            num, color_name = color.strip().split(" ") # ["1", "red"]
            if int(num) > max_values[color_name]:
                return False
    return True


def task1(data):
    '''
    Solution for task 1.
    '''
    sol = 0
    # Enumerate lines from 1 onwards. If the game is legal, add its id value to the  total sum
    for game_id, line in enumerate(data,start=1):
        legal = is_game_legal(line)
        if legal:
            sol += game_id
    return sol


def minimum_no_blocks(line):
    '''
    Function determines the least number of blocks of each color with which the game would have been legal.
    @param line: One line from the input file. Has a format of
        "Game 0: 1 red, 3 green, 5 blue; 2 red, 8 green, 7 blue"
    @returns: Dictionary containing the minimal amount of blocks:
        {'red': red_no, 'green': green_no, 'blue': blue_no}
    '''
    min_numbers = {'red': 0, 'green': 0, 'blue': 0}

    _, game_data = line.split(":")  # First split: ["Game 0", "1 red, 3 green, 5 blue; 2 red, 8 green, 7 blue"]
    runs = game_data.split(";")                 # ["1 red, 3 green, 5 blue", "2 red, 8 green, 7 blue"]
    for run in runs:
        colors = run.split(",")                 # ["1 red", "3 green", "5 blue"]
        for color in colors:
            num, color_name = color.strip().split(" ") # ["1", "red"]
            num = int(num)
            if num > min_numbers[color_name]:
                min_numbers[color_name] = num
    return min_numbers

def task2(data):
    '''
    Solution for task 2.
    '''
    sol = 0
    # For each game, determine the minimal amount of blocks, multiply those values, and add them to sum
    for line in data:
        min_blocks = minimum_no_blocks(line)
        sol += min_blocks['red'] * min_blocks['green'] * min_blocks['blue']
    return sol


# =========================

if  __name__ == "__main__":
    fn = get_fn()
    data = load_file(fn)
    print(f"Solution for task 1: {task1(data)}")
    print(f"Solution for task 2: {task2(data)}")