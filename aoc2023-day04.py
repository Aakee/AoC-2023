# -*- coding: utf-8 -*-
'''
=====
ABOUT
=====

Solution for the Advent of Coding 2023, day 4 challenge.
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
FILENAME = "./inputs/day04.txt"


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

class Card:
    '''
    Class mainly to conveniently hold data of one scratch card.
    '''
    def __init__(self, winning_numbers, card_numbers):
        self.winning_numbers    = winning_numbers
        self.card_numbers       = card_numbers
        self.matches            = None
    
    def calculate_matches(self):
        '''
        Method returns how many matches it has between its numbers and the winning numbers.
        '''
        if self.matches is None:    # If not calculated yet, calculate the number now
            self.matches = len([num for num in self.card_numbers if num in self.winning_numbers])
        return self.matches
    
    def __repr__(self) -> str:
        return f"Winning numbers: {''.join(str(self.winning_numbers))}, card numbers: {''.join(str(self.card_numbers))}"
    

def parse_line(line):
    '''
    Function parses one line of the input file and returns the card id and a respective Card object.
    '''
    header, vals    = line.split(":")
    header          = header.split(" ")
    card_id         = int(header[-1].strip())
    winning_numbers, card_numbers = vals.split("|")
    winning_numbers = winning_numbers.split(" ")
    winning_numbers = [int(val) for val in winning_numbers if val != '']
    card_numbers    = card_numbers.split(" ")
    card_numbers    = [int(val) for val in card_numbers if val != '']
    return card_id, Card(winning_numbers, card_numbers)

def parse_data(data):
    '''
    Function parses the input data file contents.
    Returns a dictionary with card_id as the key and the corresponding Card object as the value.
    '''
    cards = {}
    for line in data:
        try:
            card_id, card = parse_line(line)
            cards[card_id] = card
        except ValueError:
            continue
    return cards


def calculate_card_points(card):
    '''
    Function calculates points given by a card, according to task 1 rules.
    '''
    n_matches = card.calculate_matches()
    if n_matches == 0:
        return 0
    return 2 ** (n_matches-1)

def task1(cards):
    '''
    Solves and returns the solution for task 1.
    '''
    total_points = 0
    for _, card in cards.items():
        total_points += calculate_card_points(card)
    return total_points

def task2(cards):
    '''
    Solves and returns the solution for task 2.
    '''
    # Dictionary telling how many copies of each card we have (original included)
    nof_copies = {}
    for card_id in cards:
        nof_copies[card_id] = 1

    # Loop through each card
    for card_id, card in cards.items():
        n_copies = nof_copies[card_id]
        n_matches = card.calculate_matches()

        # For the next 'n_matches' cards, add copies corresponding to how many copies this card had
        for other_card_id in range(card_id+1, card_id + n_matches+1):
            try:
                nof_copies[other_card_id] += n_copies

            # It was guaranteed from the assignment that cards "outside the table" would never be copied,
            # but this is here just to be safe
            except KeyError:
                continue

    # Calculate and return the total number of cards
    total_number_cards = 0
    for card_id, num in nof_copies.items():
        total_number_cards += num
    
    return total_number_cards

# =========================

if  __name__ == "__main__":
    fn = get_fn()
    data = load_file(fn)
    cards = parse_data(data)

    task1_points = task1(cards)
    print(f"Task 1 solution: {task1_points} points")

    task2_num_cards = task2(cards)
    print(f"Task 2 solution: {task2_num_cards} cards")