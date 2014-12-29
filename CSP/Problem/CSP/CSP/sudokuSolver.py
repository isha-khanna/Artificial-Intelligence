# SUDOKU SOLVER

import sys
from time import time
from sudokuUtil import *

# Please implement function solve_puzzle
# input puzzle: 2D list, for example:
# [ [0,9,5,0,3,2,0,6,4]
#   [0,0,0,0,6,0,1,0,0]
#   [6,0,0,0,0,0,0,0,0]
#   [2,0,0,9,0,3,0,0,6]
#   [0,7,6,0,0,0,0,0,3]
#   [3,0,0,0,0,0,0,0,0]
#   [9,0,0,5,0,4,7,0,1]
#   [0,5,0,0,2,1,0,9,0]
#   [0,0,8,0,0,6,3,0,5] ]
# Return a 2D list with all 0s replaced by 1 to 9.
# You can utilize argv to distinguish between algorithms
# (basic backtracking or with MRV and forward checking).
# For example: python sudokuSolver.py backtracking


def solve(puzzle):
    list =[ -1, -1]
    if not unassignedLocation(puzzle, list):
        return puzzle
    
    print list[0], list[1]
    for number in range(1,10):
        if isSafe(puzzle, list[0], list[1], number):
            puzzle[list[0]][list[1]] = number
            if solve(puzzle):
                return True
            puzzle[list[0]][list[1]] = 0
            
    return False

def unassignedLocation(puzzle, list):
    rows = len(puzzle)
    cols = len(puzzle[0])
    for row in xrange(rows):
        for col in xrange(cols):
            if (puzzle[row][col] == 0):
                list[0] = row
                list[1] = col
                return True

def isSafe(puzzle, row, col, number):
    if not usedinRow(puzzle, row, number) and not usedinColumn(puzzle, col, number) and not usedinSubSquare(puzzle, row-row%3, col-col%3, number):
        return True
    return False
    
def usedinRow(puzzle, row, number):
    cols= len(puzzle[0])
    for col in xrange(cols):
        if(puzzle[row][col]==number):
            return True
    return False

def usedinColumn(puzzle, column, number):
    rows= len(puzzle)
    for row in xrange(rows):
        if(puzzle[row][column]==number):
            return True
    return False

def usedinSubSquare(puzzle, startRow, startColumn, number):
    for row in range(0,3):
        for col in range(0,3):
            if(puzzle[row+startRow][col+startColumn]==number):
                return True
    return False
    

def solve_puzzle(puzzle, argv):
    """Solve the sudoku puzzle."""

    if solve(puzzle):
        return puzzle
    else:
        print "Solution not feasible"
        
    
    
    return load_sudoku('given_solution.txt')

#===================================================#
puzzle = load_sudoku('puzzle.txt')

print "solving ..."
t0 = time()
solution = solve_puzzle(puzzle, sys.argv)
t1 = time()
print "completed. time usage: %f" %(t1 - t0), "secs."

save_sudoku('solution.txt', solution)
