# -*- coding: utf-8 -*-
'''
=====
ABOUT
=====

Solution for the Advent of Coding 2023, day 23 challenge.
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
import queue


# Type the path to your input text file here if you do not wish to use the command line argument
FILENAME = "./inputs/day23.txt"

DIRECTIONS = ((-1,0),(1,0),(0,-1),(0,1))
SLOPES     = {'^': (-1, 0),
              'v': ( 1, 0),
              '<': ( 0,-1),
              '>': ( 0, 1)}



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
    return [line for line in ret.split('\n') if line.strip() != '']

# =========================

def get_start_coordinates(maze):
    col = maze[0].index('.')
    return 0, col

def get_end_coordinates(maze):
    col = maze[-1].index('.')
    return len(maze)-1, col

def maze_object(maze,row,col):
    '''
    Returns the character in the given coordinates, or None if the coordinates are out of the maze
    '''
    if 0 <= row < len(maze) and 0 <= col < len(maze[0]):
        return maze[row][col]
    return None

def find_paths(maze, slippery=True):
    '''
    Finds and returns all paths through the maze with abreadth-first search.
    @param slippery:    True -> the tiles with an arrow (^, >, v, <) can also be gone through to the pointed direction
                        False -> the arrows are considered to be regular tiles (.) and can be traversed to any direction
    '''
    # Initialization
    q = collections.deque()
    all_paths = []
    start_row,  start_col   = get_start_coordinates(maze)
    end_row,    end_col     = get_end_coordinates(maze)

    # Format in q: each entry has form ((current_row, current_column),path_thus_far), the path_thus_far being a list of (row,col) pairs of the path
    q.append(((start_row, start_col), [(start_row, start_col)]))

    # Conducting the breadth-first search
    while len(q) > 0:
        (row, col), path = q.pop()

        # Reached goal tile -> save to all_paths and continue to next
        if row == end_row and col == end_col:
            all_paths.append(list(path))
            continue
        
        # Determine the directions we can go from this tile: if a basic tile or not slippery, any direction is applicable.
        # If slippery and an slope tile, only applicable direction is the one where the slope is pointing to
        current_tile = maze_object(maze, row, col)
        if current_tile in SLOPES and slippery:
            next_directions = (SLOPES[current_tile],)
        else:
            next_directions = DIRECTIONS

        # Loop through each (applicable) direction
        for direction in next_directions:
            
            new_row = row + direction[0]
            new_col = col + direction[1]
            new_obj = maze_object(maze, new_row, new_col)

            # Skip if the next tile would either be a wall or out of bounds, or if the tile already exists in the path
            if new_obj == '#' or new_obj is None:
                continue
            if (new_row, new_col) in path:
                continue

            # Add the new coordinates and path to these coordinates to the que
            new_path = list(path)
            new_path.append((new_row, new_col))
            q.append(((new_row, new_col), new_path))

    return all_paths


class Graph:
    '''
    Helper function to reduce the dimensionality of the maze. This is done by denoting all tiles where three or more paths meet as a 'Node', and grouping the tiles
    between two adjacent nodes as a single 'Edge'
    '''
    def __init__(self,maze) -> None:
        self.maze = maze
        self.nodes = []
        self.node_coordinates = {}
        self.create_nodes()
        self.connect_nodes()
        self.connections = {}


    def create_nodes(self):
        '''
        Find the 'nodes' from the maze (i.e. tiles with at least 3 neighbouring tiles, not counting walls)
        '''
        self.nodes = []
        start_row,  start_col   = get_start_coordinates(maze)
        end_row,    end_col     = get_end_coordinates(maze)
        self.nodes.append(Node(start_row, start_col))
        self.nodes.append(Node(end_row, end_col))

        # Loop through each coordinate in the maze
        for row, col in itertools.product(list(range(len(maze))), list(range(len(maze[0])))):
            obj = maze_object(self.maze, row, col)

            # Wall -> continue to next
            if obj == "#":
                continue

            # Not a wall -> count the number of 'neighbours', i.e. tiles that are not walls (or out of bounds)
            n_neighbours = 0
            for direction in DIRECTIONS:
                neighbour = maze_object(self.maze, row + direction[0], col + direction[1])
                if neighbour != "#" and neighbour is not None:
                    n_neighbours += 1

            # At least 3 neighbours -> mark this tile as a 'Node'
            if n_neighbours >= 3:
                self.nodes.append(Node(row, col))
        
        # Collect the coordinates for each Node
        for node in self.nodes:
            self.node_coordinates[f"{node.row},{node.col}"] = node

    def is_node(self, row, col):
        '''
        Returns True if there is a Node in the given coordinates, False if not
        '''
        return f"{row},{col}" in self.node_coordinates
    
    def node_in(self, row, col):
        '''
        Returns the Node object that lies in the given coordinates
        '''
        return self.node_coordinates[f"{row},{col}"]

    def connect_nodes(self):
        '''
        Method 'connects' the Nodes in the Graph: it finds the number of tiles between these two Nodes and froups the as a single Edge
        '''
        self.edges = []

        # Method: Iterate through each node. Start going to all directions from this node (obviously stopping at walls) and find the node where this path connects to.
        for node, direction in itertools.product(self.nodes, DIRECTIONS):
            path = [[node.row, node.col]]

            # First: Find if this direction is applicable in the first place (there is not a wall in the very next tile starting from the Node)
            row, col = node.row + direction[0], node.col + direction[1]
            next_obj = maze_object(self.maze, row, col)
            if next_obj in ('#', None):
                continue

            # Follow the path until either another Node is found, or the path hits a dead end
            path.append([row, col])
            while not self.is_node(row, col):
                for d in DIRECTIONS:
                    next_row, next_col = row + d[0], col + d[1]
                    next_obj = maze_object(self.maze, next_row, next_col)
                    
                    # Find the "correct" direction, that is, the only direction which is not already in the path and which is not a wall
                    if next_obj not in ('#', None) and [next_row, next_col] not in path:
                        break
                
                path.append([next_row, next_col])
                row, col = next_row, next_col

            # Construct an Edge between the two Nodes
            other_node = self.node_in(row,col)
            e = Edge(node, other_node, len(path)-1, path)
            node.connects_to[other_node] = e
            self.edges.append(e)


    def path_length(self, path):
        length = 0
        for first, second in zip(path[:-1], path[1:]):
            length += first.connects_to[second].weight
        return length

    def find_longest_path(self):
        '''
        Method finds the longest path in the graph and returns its length
        '''
        start_row,  start_col   = get_start_coordinates(maze)
        end_row,    end_col     = get_end_coordinates(maze)
        
        start = self.node_in(start_row, start_col)
        goal  = self.node_in(end_row, end_col)


        q = collections.deque()
        q.append([start])

        longest_path_length = 0

        # Conduct a breadth-first search to iterate through all paths, and keep track of the longest found path
        while len(q) > 0:
            path = q.pop()
            node = path[-1]
            if node == goal:
                length = self.path_length(path)
                longest_path_length = max(longest_path_length, length)
                continue
            for next_node, next_edge in node.connects_to.items():
                if next_node in path:
                    continue
                new_path = list(path)
                new_path.append(next_node)
                q.append(new_path)

        return longest_path_length



class Node:
    '''
    Data class holding the information of a Node in the graph
    '''
    def __init__(self, row, col) -> None:
        self.row = row
        self.col = col
        self.connects_to = {}

    def __repr__(self) -> str:
        return f"({self.row},{self.col})"


class Edge:
    '''
    Data class holding information about the Edge between two Nodes
    '''
    def __init__(self,first_node, second_node ,weight, path=[]) -> None:
        self.first = first_node
        self.second = second_node
        self.weight= weight
        self.path = path

    def __repr__(self) -> str:
        return f"{self.first}->{self.second};{self.weight}"
    
# =========================

def part1(maze: list) -> int:
    '''
    Solution for the part 1.
    '''
    all_paths = find_paths(maze, slippery=True)
    all_paths.sort(key=lambda path: len(path))

    return len(all_paths[-1])-1


def part2(maze: list) -> int:
    '''
    Solution for the part 2.
    '''
    g = Graph(maze)
    length = g.find_longest_path()
    return length

# =========================

if  __name__ == "__main__":
    fn = get_fn()
    maze = load_file(fn)

    print(f"Part 1 solution: {part1(maze)}")
    print(f"Part 2 solution: {part2(maze)}")