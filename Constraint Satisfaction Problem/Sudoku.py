# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 14:08:49 2021

@author: mjvat
"""
import sys
import queue
from copy import deepcopy

rows = "ABCDEFGHI"
cols = "123456789"
boxes = ""

def combine(rows, cols):
    return [a + b for a in rows for b in cols]

boxes = combine(rows, cols)

class Sudoku:
    
    def __init__ (self, domain=cols, grid=""):
        
        boxes = combine(rows, cols)
        self.boxes = boxes
        self.domain = self.boardConfig(grid)
        self.values = self.boardConfig(grid)
        self.combined = combine(rows, cols)
        self.constraintDomain = (
            [combine(r, cols) for r in rows] +
            [combine(rows, c) for c in cols] +
            [combine(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])
        
        self.conValues = dict((b, [cv for cv in self.constraintDomain if b in cv]) for b in boxes)
        self.neighbors = dict((b, set(sum(self.conValues[b],[]))-set([b])) for b in boxes)
        self.constraints = {(inp, neighbor) for inp in self.boxes for neighbor in self.neighbors[inp]}
    
    def boardConfig(self, grid=""):
    	i = 0
    	values = dict()
    	for cell in self.boxes:
    		if grid[i]!='0':
    			values[cell] = grid[i]
    		else:
    			values[cell] = cols
    		i = i + 1
    	return values
    
# AC3
def AC3(constraint):
    
    ac3q = queue.Queue()

    for i in constraint.constraints:
        ac3q.put(i)

    c = 0
    while not ac3q.empty():
        (x, y) = ac3q.get()

        c = c + 1

        if alter(constraint, x, y):
            if len(constraint.values[x]) == 0:
                return False
            for ii in (constraint.neighbors[x] - set(y)):
                ac3q.put((ii, x))

    return(constraint.values)
    return True
    
def alter(constraint, x, y):
    
    altered = False
    values = set(constraint.values[x])

    for i in values:
        if not acConsistent(constraint, x, x, y):
            constraint.values[x] = constraint.values[x].replace(i, '')
            altered = True

    return altered

def acConsistent(constraint, x, y, z):
    for i in constraint.values[z]:
        if z in constraint.neighbors[y] and i != x:
            return True

    return False

def acComplete(constraint):
    for variable in boxes:
        if len(constraint.values[variable]) > 1:
            return False
    return True

# Backtracking
def backtrackSearch(constraint):
    return backtrack({}, constraint)

def backtrack(inputs, constraint):
    if bsComplete(inputs):
        return inputs

    var = variables(inputs, constraint)
    domain = deepcopy(constraint.values)

    for i in constraint.values[var]:
        if bsConsistent(var, i, inputs, constraint):
            inputs[var] = i
            inferences = {}
            inferences = Inference(inputs, inferences, constraint, var, i)
            if inferences != "Failure":
                result = backtrack(inputs, constraint)
                if result != "Failure":
                    return result

            del inputs[var]
            constraint.values.update(domain)

    return "Failure"

def Inference(inputs, inferences, constraint, var, value):
    inferences[var] = value

    for neighbor in constraint.peers[var]:
        if neighbor not in inputs and value in constraint.values[neighbor]:
            if len(constraint.values[neighbor]) == 1:
                return "FAILURE"

            remaining = constraint.values[neighbor] = constraint.values[neighbor].replace(value, "")

            if len(remaining) == 1:
                flag = Inference(inputs, inferences, constraint, neighbor, remaining)
                if flag == "Failure":
                    return "Failure"

    return inferences

def bsComplete(inputs):
    return set(inputs.keys()) == set(boxes)

def variables(inputs, constraint):
    unassigned_variables = dict(
        (boxes, len(constraint.values[boxes])) for boxes in constraint.values if boxes not in inputs.keys())
    mrv = min(unassigned_variables, key=unassigned_variables.get)
    return mrv

def forwardCheck(constraint, inputs, var, value):
    constraint.values[var] = value
    for neighbor in constraint.neighbors[var]:
        constraint.values[neighbor] = constraint.values[neighbor].replace(value, '')

def orderValues(var, inputs, constraint):
    return constraint.values[var]

def bsConsistent(var, value, inputs, constraint):
    for neighbor in constraint.neighbors[var]:
        if neighbor in inputs.keys() and inputs[neighbor] == value:
            return False
    return True

def write(results):
    output = ""
    for i in boxes:
        output += results[i]
    return output

if __name__ == "__main__":

    layout = '000000000302540000050301070000000004409006005023054790000000050700810000080060009'
    assert len(layout) == 81
    game = Sudoku(grid=layout)
    
    f = open('output.txt','w')
    assignment = AC3(game)
    
    if acComplete(game) and assignment:
        f.write(write(assignment) + ' AC3' + '\n')
    else:
        assignment = backtrackSearch(game)
        f.write(write(assignment) + ' BTS' + '\n')
        
    f.close()
    
    
    '''
    if len(sys.argv)==2:
        layout = sys.argv[1]
        assert len(layout) == 81        
        game = Sudoku(grid=layout)
    
        f = open("output.txt", "w")
        assignment = AC3(game)
    
        if acComplete(game) and assignment:
            f.write(write(assignment) + " AC3" + "\n")    
        
    else:
        assignment = backtrackSearch(game)
        f.write(write(assignment) + " BTS" + "\n")

    f.close()
    '''
    

