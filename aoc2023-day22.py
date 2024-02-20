# -*- coding: utf-8 -*-
'''
=====
ABOUT
=====

Solution for the Advent of Coding 2023, day 22 challenge.
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
import copy


# Type the path to your input text file here if you do not wish to use the command line argument
FILENAME = "./inputs/day22.txt"


def get_fn() ->  str:
    '''
    Function extracts the input file from the commandline argument, if given.
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

def c2str(coordinates):
    '''
    Function converts given coordinates to a string.
    @param coordinates: List or tuple in format (x,y,z)
    @returns: string in format "x,y,z"
    '''
    return f"{coordinates[0]},{coordinates[1]},{coordinates[2]}"

class BrickManager:
    '''
    Class stores a collection of bricks and handles their operations.
    '''
    def __init__(self) -> None:
        self.bricks = []    # all bricks in the system
        self.grid   = []    # a three-dimensional list denoting the (x,y,z) coordinates of the whole system

    def new_brick(self, brick):
        '''
        Method adds the given brick to the list self.bricks
        '''
        self.bricks.append(brick)

    def remove_brick(self, brick):
        '''
        Method removes the given brick from the self.grid.
        The method DOES NOT check if the return value of brick.occupies() actually matches the brick's coordinates in self.grid!
        '''
        for x,y,z in brick.occupies():
            self.grid[x][y][z] = None

    def delete_brick(self, brick):
        '''
        Method deletes the brick from the system: it removes the brick from the list self.bricks and from self.grid (with the help of method BrickManager.remove_brick() )
        '''
        self.remove_brick(brick)
        self.bricks.remove(brick)

    def get_extreme_values(self):
        '''
        Method returns the 'extreme values' of the system, that is, the minimum and maximum value of each coordinate that exists in the system.
        This means that for all bricks b it holds that min_x <= b.x <= max_x, and same for x and y.
        '''
        max_x, max_y, max_z = -math.inf, -math.inf, -math.inf
        min_x, min_y, min_z =  math.inf,  math.inf,  math.inf
        for brick in self.bricks:
            min_x = min(min_x, brick.x[0])
            min_y = min(min_y, brick.y[0])
            min_z = min(min_z, brick.z[0])
            max_x = max(max_x, brick.x[1])
            max_y = max(max_y, brick.y[1])
            max_z = max(max_z, brick.z[1])
        return (min_x, min_y, min_z, max_x, max_y, max_z)
    

    def move_brick_to_direction(self, brick, xdelta=0, ydelta=0, zdelta=0):
        '''
        Method TRIES TO move the given brick to the given direction a given amount of steps.
        This means that the method first checks if the movement is legal (for one step), and only moves the brick if it is.
        Note that the check currently only checks that the resulting space is empty; it does not care if the brick would jump over some bricks to reach the new position.
        @param xdelta, ydelta, zdelta: Desired steps that the brick would be moved to x/y/z direction.
        @returns: True if the movement was succesful, False if the movement was illegal and was not executed.
        '''
        currently_occupies = brick.occupies()

        # Check that the movement is legal
        try:
            for x,y,z in currently_occupies:
                # Check that the resulting space is empty or already contains the brick in question.
                # The latter check is to allow vertical blocks to still move downwards (and also horizontal bricks to move to horizontal direction);
                # the brick is allowed to go to a space that the brick itself was already occupying.
                if self.grid[x+xdelta][y+ydelta][z+zdelta] not in (None, brick): # Raises IndexError if out of bounds
                    return False
                # Check that the brick would not be moved below ground level
                if z+zdelta < 1:
                    return False
        except IndexError:
            return False
            
        # Remove the brick from the grid
        self.remove_brick(brick)

        # Update brick coordinates
        brick.x = (brick.x[0]+xdelta, brick.x[1]+xdelta)
        brick.y = (brick.y[0]+ydelta, brick.y[1]+ydelta)
        brick.z = (brick.z[0]+zdelta, brick.z[1]+zdelta)

        # Place new brick coordinates to grid
        self.place_brick_to_grid(brick)

        return True


    def construct_grid(self):
        '''
        Method recreates the three-dimensional list self.grid and places all bricks into it.
        '''
        min_x, min_y, min_z, max_x, max_y, max_z = self.get_extreme_values()
        self.grid= [[[None for z in range(min_z,max_z+3)] for y in range(min_y,max_y+1)] for x in range(min_x, max_x+1)]
        for brick in self.bricks:
            self.place_brick_to_grid(brick)


    def place_brick_to_grid(self, brick):
        '''
        Method places the given brick to self.grid.
        Raises ValueError if the placement couldn't be completed due to the space already being occupied.
        '''
        for x,y,z in brick.occupies():
            if self.grid[x][y][z] is not None:
                raise ValueError
            self.grid[x][y][z] = brick


    def apply_gravity(self):
        '''
        Method moves all bricks downwards, i.e. to negative z direction, until they all rest either on ground or on top of another brick.
        '''
        # Re-construct the grid and initialize values
        self.construct_grid()
        min_x, min_y, min_z, max_x, max_y, max_z = self.get_extreme_values()
        processed_bricks = []
        
        # Number of brick that moves when applying gravity
        n_would_fall = 0

        # Loop through the grid level by level, from bottom to top, and on each level through all xy-coordinates.
        # Point is that when starting from bottom, no such problems appear that a brick should be moved twice due to it first hitting another brick but this
        # supporting brick also moved later.
        for z in range(min_z, max_z+1):
            for x,y in itertools.product(list(range(min_x, max_x+1)), list(range(min_y, max_y+1))):

                # Skip if the space is empty
                if self.grid[x][y][z] is None:
                    continue

                # Skip if the brick in the space has already been processed
                if self.grid[x][y][z] in processed_bricks:
                    continue

                # Collect the brick and apply gravity to the brick
                brick = self.grid[x][y][z]
                ret = True
                counted = False

                # Move the brick downwards until it can no longer be moved (= until self.move_brick_to_direction returns False)
                while ret:
                    ret = self.move_brick_to_direction(brick,zdelta=-1)
                    
                    # If the brick moved and it was not yet been counted to the total, cont this brick to the total sum
                    if ret and not counted:
                        n_would_fall += 1
                        counted = True

                # Mark this brick as processed (no need to check for gravity again)
                processed_bricks.append(brick)
        
        return n_would_fall

            

class Brick:
    '''
    Data class holding the location information of a single brick
    '''
    def __init__(self, x0, y0, z0, x1, y1, z1) -> None:
        self.x = (min(int(x0),int(x1)),max(int(x0),int(x1)))
        self.y = (min(int(y0),int(y1)),max(int(y0),int(y1)))
        self.z = (min(int(z0),int(z1)),max(int(z0),int(z1)))

    def occupies(self):
        '''
        Returns a list of coordinates where this brick is places.
        All squares where the brick goes through are counted, not just the extremes.
        For example, [(0,0,1),(0,0,2),(0,0,3)]
        '''
        return [(x,y,z) for x in range(self.x[0], self.x[1]+1) for y in range(self.y[0], self.y[1]+1) for z in range(self.z[0], self.z[1]+1)]
    
    def __repr__(self) -> str:
        return f"{self.z[0]}"
    

def create_bricks(data):
    '''
    Function parses the input data to create the Brick objects, and adds them to a BrickManager.
    '''
    bm = BrickManager()
    for line in data:
        if  line.strip() == "":
            continue
        c0, c1 = line.split('~')
        x0,y0,z0 = c0.split(',')
        x1,y1,z1 = c1.split(',')
        bm.new_brick(Brick(x0,y0,z0,x1,y1,z1))
    return bm

def verify_gravity(bm):
    '''
    Function verifies that gravity is applied correctly, i.e. no brick can be moved downwards. Useful for testing and debugging.
    Returns True if gravity has been applied correctly, False if at least one brick could be moved downwards.
    '''
    bm_copy = copy.deepcopy(bm)
    for brick in bm_copy.bricks:
        ret = bm_copy.move_brick_to_direction(brick, zdelta=-1)
        if ret:
            return False
    return True



# =========================

def part1(bm) -> int:

    '''
    Solution for the part 1.
    '''
    min_x, min_y, min_z, max_x, max_y, max_z = bm.get_extreme_values()

    # Maps bricks from supporting brick to bricks it supports: supports[a]=[b,c,d] means that brick a supports bricks b, c and d
    supports        = {}

    # Maps bricks from supported bricks to bricks they are supported by: is_supported_by[a]=[b,c,d] means that brick a is supported by bricks b, c and d
    is_supported_by = {}

    # Initialize the dictionaries
    for brick in bm.bricks:
        supports[brick]         = []
        is_supported_by[brick]  = []

    # Loop for every height, starting from bottom
    for z in range(1, max_z+2):
        # Loop for all xy-coordinates
        for x,y in itertools.product(list(range(min_x, max_x+1)),list(range(min_y, max_y+1))):
            btm = bm.grid[x][y][z-1]
            top = bm.grid[x][y][z]

            # If there is a brick on coordinates 'btm' and another at 'top', then brick at btm supports the brick at top -> register this to the dictionaries
            if btm is not None and top is not None and btm != top:
                if top not in supports[btm]:
                    supports[btm].append(top)
                if btm not in is_supported_by[top]:
                    is_supported_by[top].append(btm)

    n_can_be_taken = 0
    
    # Loop through each brick to see if they can be taken
    for btm in bm.bricks:
        can_be_taken = True

        # Check through each brick the bottom brick supports.
        # If each of them has at least some other brick supporting it, the bottom brick can safely be removed.
        for top in supports[btm]:
            tmp = list(is_supported_by[top])
            tmp.remove(btm)
            if len(tmp) == 0:
                can_be_taken = False
                break
        if can_be_taken:
            n_can_be_taken += 1

    return n_can_be_taken



def part2(bm) -> int:
    '''
    Solution for the part 2.
    '''
    tot = 0

    # Loop through each brick and find how many bricks would fall if this brick were removed
    for idx in range(len(bm.bricks)):
        bm_copy = copy.deepcopy(bm)     # deepcopy -> the original stays intact
        bm_copy.delete_brick(bm_copy.bricks[idx])
        tot += bm_copy.apply_gravity()

    return tot


# =========================

if  __name__ == "__main__":
    
    fn = get_fn()
    data = load_file(fn)
    
    bm = create_bricks(data)
    bm.construct_grid()
    bm.apply_gravity()

    print(f"Part 1 solution: {part1(bm)}")

    # The part 2 solution is quite slow, but the time it takes is still reasonable to wait out (around 40 seconds for me)
    print(f"Part 2 solution: {part2(bm)}")
