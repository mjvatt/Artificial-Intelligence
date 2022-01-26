# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 00:46:22 2021

Project 1 of Columbia University's AI EdX course (8-puzzle).

@author: mjvat
"""

import sys 
import heapq 
import queue as q
import time
import math
from dataclasses import dataclass, field
from typing import Any
import psutil
@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any=field(compare=False)
    
### 8-Puzzle Game ###
## The Class that Represents the Puzzle
# The skeleton code given to us to start from for the project
class PuzzleState(object):

    def __init__(self, config, n, parent=None, action="Initial", cost=0):

        if n * n != len(config) or n < 2:
            raise Exception("the length of config is not correct!")

        self.n = n
        self.cost = cost
        self.parent = parent
        self.action = action
        self.dimension = n
        self.config = config
        self.children = []

        for i, item in enumerate(self.config):
            if item == 0:
                self.blank_row = i // self.n
                self.blank_col = i % self.n
                break    
            
    # To allow a "'<' not supported between instances" error to be overridden and successfully compile
    def __lt__(self, other):
        return calculate_total_cost(self) < calculate_total_cost(other)

    def display(self):
        for i in range(self.n):
            line = []
            offset = i * self.n
            for j in range(self.n):
                line.append(self.config[offset + j])
            print(line)

    def move_left(self):
        if self.blank_col == 0:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index - 1
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Left", cost=self.cost + 1)

    def move_right(self):
        if self.blank_col == self.n - 1:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index + 1
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Right", cost=self.cost + 1)

    def move_up(self):
        if self.blank_row == 0:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index - self.n
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Up", cost=self.cost + 1)

    def move_down(self):
        if self.blank_row == self.n - 1:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index + self.n
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Down", cost=self.cost + 1)

    def expand(self):
        """expand the node"""

        # add child nodes in order of UDLR
        if len(self.children) == 0:
            up_child = self.move_up()

            if up_child is not None:
                self.children.append(up_child)

            down_child = self.move_down()

            if down_child is not None:
                self.children.append(down_child)

            left_child = self.move_left()

            if left_child is not None:
                self.children.append(left_child)

            right_child = self.move_right()

            if right_child is not None:
                self.children.append(right_child)

        return self.children

# To perform a BFS search on the puzzle state
def bfs_search(initial_state):

    start_timer = time.time()
    
    explored_nodes = 0
    max_search_depth = 0
    
    frontier = q.Queue()
    frontier.put(initial_state)

    explored = set()
    explored.add(initial_state.config)

    while(frontier!=None): 
        state = frontier.get()

        if (test_goal(state)):
            search_depth = state.cost
            running_time = time.time() - start_timer
            max_ram_usage = psutil.Process().memory_info().rss/1048576
            writeOutput(state, explored_nodes, search_depth, max_search_depth, running_time, max_ram_usage)
            break

        state.expand()
        explored_nodes += 1

        for i in state.children:
            if (i.config in explored):
                pass
            else:
                if (i.cost > max_search_depth):
                    max_search_depth = i.cost
                frontier.put(i)
                explored.add(i.config)


# To perform a DFS search on the puzzle state
def dfs_search(initial_state):

    start_timer = time.time()

    explored_nodes = 0
    max_search_depth = 0
    
    frontier = q.LifoQueue()
    frontier.put(initial_state)

    explored = set()
    explored.add(initial_state.config)

    while(frontier!=None):
        state = frontier.get()

        if (test_goal(state)):
            search_depth = state.cost
            running_time = time.time() - start_timer
            max_ram_usage = psutil.Process().memory_info().rss/1048576
            writeOutput(state, explored_nodes, search_depth, max_search_depth, running_time, max_ram_usage)
            break

        state.expand()
        state.children.reverse()
        explored_nodes += 1

        for i in state.children:
            if (i.config in explored):
                pass
            else:
                if (i.cost > max_search_depth):
                    max_search_depth = i.cost
                frontier.put(i)
                explored.add(i.config)

# To perform an A* search on the puzzle state
def A_star_search(initial_state):

    start_timer = time.time()
    
    explored_nodes = 0
    max_search_depth = 0
    
    frontier = [initial_state]
    heapq.heapify(frontier)
    frontier_configs = set(initial_state.config)
    
    explored = set()
    explored.add(initial_state.config)
    
    while(frontier!=None):
        state = heapq.heappop(frontier)
        
        if (test_goal(state)):
            search_depth = state.cost
            running_time = time.time() - start_timer
            max_ram_usage = psutil.Process().memory_info().rss/1048576
            writeOutput(state, explored_nodes, search_depth, max_search_depth, running_time, max_ram_usage)
            break
        
        state.expand()
        explored.add(state.config)
        explored_nodes += 1
        
        for i in state.children:
            if not i.config in frontier_configs and not i.config in explored:
                heapq.heappush(frontier, i)
                frontier_configs.add(i.config)
                if i.cost > max_search_depth:
                    max_search_depth = i.cost
                
# To calculate the total cost of the path
def calculate_total_cost(state):

    cost = 0
    while(state.parent!=None):
        cost += 1
        state = state.parent
    
    return cost

# To calculate the manhattan distance
def calculate_manhattan_dist(idx, value, n):

    manhattan = 0
    manhattan = abs((idx % n) - (value % n)) + abs((idx // n) - (value // n))
    return manhattan

# To determine if the state is the goal state or not
def test_goal(state):

    if state.config == tuple(range(state.n**2)):
        return True

# To write the results of the algorithm to an output file 'output.txt'
def writeOutput(puzzle, explored_nodes, search_depth, max_search_depth, running_time, max_ram_usage):
    
    moves = []
    cost = puzzle.cost
    
    while(puzzle.parent!=None):
        moves.append(puzzle.action)
        puzzle = puzzle.parent
    
    moves.reverse()
    
    # Solely prints to the Python console to verify it is working properly
    with open("output.txt",'w') as output_file:
        print("path_to_goal: {0}".format(moves))
        print("cost_of_path: {0}".format(cost))
        print("nodes_expanded: {0}".format(explored_nodes))
        print("search_depth: {0}".format(search_depth))
        print("max_search_depth: {0}".format(max_search_depth))
        print("running_time: {0}".format(running_time))
        print("max_ram_usage: {0}".format(max_ram_usage))

        # Writes to output.txt file
        output_file.write("path_to_goal: {0}".format(moves)+"\n")
        output_file.write("cost_of_path: {0}".format(cost)+"\n")
        output_file.write("nodes_expanded: {0}".format(explored_nodes)+"\n")
        output_file.write("search_depth: {0}".format(search_depth)+"\n")
        output_file.write("max_search_depth: {0}".format(max_search_depth)+"\n")
        output_file.write("running_time: {0}".format(running_time)+"\n")
        output_file.write("max_ram_usage: {0}".format(max_ram_usage)+"\n")
        
# Main Function to read I/O and run the appropriate algorithm
def main():

    sm = sys.argv[1].lower()

    begin_state = sys.argv[2].split(",")

    begin_state = tuple(map(int, begin_state))
    size = int(math.sqrt(len(begin_state)))
    hard_state = PuzzleState(begin_state, size)

    if sm == "bfs":
        bfs_search(hard_state)
    elif sm == "dfs":
        dfs_search(hard_state)
    elif sm == "ast":
        A_star_search(hard_state)
    else:
        print("Enter valid command arguments !")
    
# Calls main function
if __name__ == '__main__':
    main()