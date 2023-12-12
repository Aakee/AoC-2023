# -*- coding: utf-8 -*-
'''
=====
ABOUT
=====

Solution for the Advent of Coding 2023, day XX challenge.
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
from typing import Any


# Type the path to your input text file here if you do not wish to use the command line argument
FILENAME = "./inputs/day07.txt"


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

class HandValues:
    '''
    Enumerations of different hand values
    '''
    FIVES       = 6
    FOURS       = 5
    FULLHOUSE   = 4
    SET         = 3
    TWOPAIRS    = 2
    PAIR        = 1
    HIGH        = 0

# Enumerations of card values in task 1
CARD_VALUES_1 = { 'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2}

# Enumerations of card values in task 2
CARD_VALUES_2 = { 'A': 14, 'K': 13, 'Q': 12, 'T': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2, 'J': 1 }

class Hand:
    '''
    Represents an instance of five cards and a bounty
    '''
    def __init__(self, cards, bounty) -> None:
        self.cards      = cards
        self.bounty     = int(bounty)
        self.hand_value = None
        self.rank       = None

    def determine_hand_value_task_1(self):
        '''
        Determines and sets thehand value according to the rules in task 1
        '''
        self.hand_value = determine_hand_value_task(self.cards, joker=False)

        # Tiebreak logic: Collect the numerical values of each of the five cards in their original order as a string; for example,
        # K29TQ would become '1302091012'. Then multiply by 1e-10 to get a decimal value less than zero, and addthis value to the base rank value.
        # Now, when comparing two hands, the main rank precedes, andthis tiebreak is used if the main rank is the same.
        tiebreak = f"{CARD_VALUES_1[self.cards[0]]:02d}{CARD_VALUES_1[self.cards[1]]:02d}{CARD_VALUES_1[self.cards[2]]:02d}{CARD_VALUES_1[self.cards[3]]:02d}{CARD_VALUES_1[self.cards[4]]:02d}"
        self.hand_value += int(tiebreak) * 1e-10

    def determine_hand_value_task_2(self):
        '''
        Determines and sets thehand value according to the rules in task 1
        '''
        self.hand_value = determine_hand_value_task(self.cards, joker=True)

        # Same tiebreak logic as in task 1, but with the alternate values (J is the least valuable as a tiebreak)
        tiebreak = f"{CARD_VALUES_2[self.cards[0]]:02d}{CARD_VALUES_2[self.cards[1]]:02d}{CARD_VALUES_2[self.cards[2]]:02d}{CARD_VALUES_2[self.cards[3]]:02d}{CARD_VALUES_2[self.cards[4]]:02d}"
        self.hand_value += int(tiebreak) * 1e-10

    def __repr__(self) -> str:
        return ''.join(self.cards)


def find_n_of_a_kind(hand: list, n: int, joker=False):
    '''
    Function searches the hand for a set of exactly n of a kind, and returns a list containing all ranks where this condition was met.
    If joker=True, treats J cards as jokers. To avoid  the same joker to be counted multiple times in multiple sets, it is removed after the first
    occurence of a set of n kind.
    '''
    ret = []
    hand = list(hand)
    for rank in ['A','K','Q','J','T','9','8','7','6','5','4','3','2']:
        sets = [card for card in hand if card == rank or (joker and card == 'J')]
        if len(sets) == n:
            ret.append(rank)
            if joker:
                hand = [card for card in hand if card != "J" and card != rank]
    return ret

def has_full_house(hand: list, joker=False):
    '''
    Function checks if the hand has a full house, and returns True if it does, and False if it does not.
    If joker=True, J is interpreted as joker.
    '''
    hand = list(hand)
    pair = False
    trips = False
    for rank in ['A','K','Q','J','T','9','8','7','6','5','4','3','2']:
        sets = [card for card in hand if card == rank or (joker and card == 'J')]
        if len(sets) == 3:
            trips = True
            if joker:
                hand = [card for card in hand if card != "J" and card != rank]
        if len(sets) == 2:
            pair = True
            if joker:
                hand = [card for card in hand if card != "J" and card != rank]  
    return trips and pair


def determine_hand_value_task(hand: list, joker=False):
    '''
    Determines and returns the value (rank) of a hand.
    If joker=True, J is treated as joker.
    '''
    if len(find_n_of_a_kind(hand, 5, joker=joker)) > 0:
        return HandValues.FIVES
    if len(find_n_of_a_kind(hand, 4, joker=joker)) > 0:
        return HandValues.FOURS
    if has_full_house(hand,joker=joker):
        return HandValues.FULLHOUSE
    if len(find_n_of_a_kind(hand, 3, joker=joker)):
        return HandValues.SET
    if len(find_n_of_a_kind(hand, 2, joker=joker)) > 1:
        return HandValues.TWOPAIRS
    if len(find_n_of_a_kind(hand, 2, joker=joker)) > 0:
        return HandValues.PAIR
    return HandValues.HIGH


def parse_data_to_hands(data):
    '''
    Function parses the input data to a list of Hand objects.
    '''
    hands = []
    for line in data:
        try:
            cards, bounty = line.split(" ")
            hand = Hand(cards=cards, bounty=bounty)
            hands.append(hand)
        except ValueError:
            pass
    return hands

def task1(hands):
    '''
    Solution to the first task
    '''
    # Determine the value of each hand
    for hand in hands:
        hand.determine_hand_value_task_1()
    
    # Sort the hands in ascending order based on their value, and rank them from 1 to n.
    # Add money to the pot equal to each hands bounty multiplied by its rank.
    hands.sort(key=lambda x: x.hand_value)
    total_bounty = 0
    for rank, hand in enumerate(hands, start=1):
        total_bounty += rank * hand.bounty

    return total_bounty


def task2(hands):
    '''
    Solution to the second task
    '''
    # Determine the value of each hand
    for hand in hands:
        hand.determine_hand_value_task_2()
    
    # Sort the hands in ascending order based on their value, and rank them from 1 to n.
    # Add money to the pot equal to each hands bounty multiplied by its rank.
    hands.sort(key=lambda x: x.hand_value)
    total_bounty = 0
    for rank, hand in enumerate(hands, start=1):
        total_bounty += rank * hand.bounty

    return total_bounty

# =========================

if  __name__ == "__main__":
    fn      = get_fn()
    data    = load_file(fn)
    hands   = parse_data_to_hands(data)

    print(f"Task 1 solution: {task1(hands)}")
    print(f"Task 2 solution: {task2(hands)}")