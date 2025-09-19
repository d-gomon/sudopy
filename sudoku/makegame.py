import random
from sudoku.ui import print_board
from typing import List, Union, Optional
import pdb
import curses

# Here we want to create a sudoku grid from scratch
# To do so, we already need some functions to check whether the grid is
# VALID

# The grid is VALID when:
# Each number is present in each row and column AT MOST once.
# Each number is present in each BLOCK (3x3) AT MOST once.

# The grids are indexed by 0-2, 3-5, 6-8 respectively

def start_game(SudokuBoard):
    if SudokuBoard.gametype == 1:
        play_game(SudokuBoard)
    elif SudokuBoard.gametype == 2:
        curses.wrapper(lambda stdscr: get_board_input(stdscr, SudokuBoard))
        solve_board(SudokuBoard)
    elif SudokuBoard.gametype == 3:
        createValidBoard(SudokuBoard)
    elif SudokuBoard.gametype == 4:
        exit()

def play_game(SudokuBoard):
    #We want the game to wait for user input as long as the sudoku puzzle is not solved
    while SudokuBoard.solved == False:
        SudokuBoard.print_board()
        SudokuBoard.play_round()
        

def get_board_input(stdscr, SudokuBoard):
    #Need to allow the user to input the sudokuboard. Would be nice if could be done using arrows.
    stdscr.clear()
    SudokuBoard.input_board(stdscr)



def solve_board(SudokuBoard):
    
    SudokuBoard.solved = False


def createValidBoard(sudokuBoard):
    #We may hit recursion limit, so we just try with different seed
    while True:
        try:
            #-----------Initialize the board, possible values and grid---------------
            board = [[None for i in range(sudokuBoard.size)] for j in range(sudokuBoard.size)] #size x size board initialization
            possible_values = [[list(range(1, sudokuBoard.size + 1)) for i in range(sudokuBoard.size)] for j in range(sudokuBoard.size)]  
            random.seed()
            #-------------DFS with backtracking-------------
            if DFS(board=board, possible_values=possible_values):
                break
        except RecursionError:
            print("Recursion limit hit. Retrying...")
    
    #Assign solution to our sudokuBoard.
    sudokuBoard.board = board
    print_board(board)
    


def DFS(board, possible_values):
    #Seeing as doing a greedy approach might yield non-feasible board, we use 
    #Depth First Search with backtracking.

    #This works as follows:
    # We define a function with as input the possible_values
    # We create a sudoku board which is completely empty
    # In possible_values, choose the coordinate with the least possible values left.
    # If the whole sudoku board is filled: return True
    # For all possible values that can be added to that coordinate:
        # Add a random possible value to that coordinate
        # If this is possible (check):
            # Update possible_values with the new entry
            # Update the board with the new value
            # re-run the solver function on the NEW possible_values and board
            # If solved, return True to exit loop
        # If this is not possible, remove the value from that coordinate and reset possible_values
    # Return False, as no possible value found in this cell.
    
    #Find least possible values coordinate
    x_coord, y_coord = find_least_empty(possible_values)
    #If such a coordinate doesn't exist, we are done
    if x_coord is None:
        if is_board_filled(board):
            return True
        else:
            return False
    
    random.shuffle(possible_values[x_coord][y_coord])
    #We try all possible values at this coordinate 
    #(we don't have to check) feasibility, because this is already done in find_least_empty
    for value in possible_values[x_coord][y_coord]:
        board[x_coord][y_coord] = value #Update coordinate value
        update_possible_values(possible_values = possible_values, x_coord = x_coord, y_coord = y_coord, value = value)
        #Go one layer deeper and check if we are at a solution.
        if DFS(board, possible_values):
            return True
        
        #If we didn't solve, backtrack (remove value from the coordinates and update the board again)
        board[x_coord][y_coord] = None
        #Unfortunately, we can't simply put the value back in the rows columns and grids 
        #as we also need to check whether there isn't another entry in the rows/columns with the same value
        #We therefore need to write a slightly more elaborate reverse_possible_values function. 
        reverse_possible_values(possible_values= possible_values, x_coord=x_coord, y_coord=y_coord, value=value, board=board)
    return False
        


def update_possible_values(possible_values, x_coord, y_coord, value):
    possible_values[x_coord][y_coord] = [] #Make empty list
    grid_idx = [set(range(0, 2 + 1)), set(range(3, 5+1)), set(range(6, 8+1))]
    #Update possible values when adding a value to x_coord, y_coord
    #Remove from ROWS:
    for col in range(9):
        if possible_values[x_coord][col] and value in possible_values[x_coord][col]:
            possible_values[x_coord][col].remove(value)
    #Remove from COLUMNS:
    for row in range(9):
        if possible_values[row][y_coord] and value in possible_values[row][y_coord]:
            possible_values[row][y_coord].remove(value)
    #Remove from nearby grid:
    grid_x = x_coord//3
    grid_y = y_coord//3
    for grid_row in grid_idx[grid_x]:
        for grid_col in grid_idx[grid_y]:
            if possible_values[grid_row][grid_col] and value in possible_values[grid_row][grid_col]:
                possible_values[grid_row][grid_col].remove(value)

def reverse_possible_values(possible_values, x_coord, y_coord, value, board):
    # Basically, we will go through the ranges where we need to add the value to possible values again,
    # BUT we will also be checking whether this value isn't already present in any of the rows/columns we are iterating over.
    # We only need to do this for the row/columns, not for the grids

    # We also need to check that the possible values ARE NOT EMPTY!! If they are empty, we do not add!

    # First, we update the original coordinate to include the value again
    possible_values[x_coord][y_coord].append(value)

    # Function to check whether a value is present in a row/column
    def present_in_board(row, column, value, board):
        if row is not None: #Check if present in a row
            if value in board[row]:
                return True
        elif column is not None:
            if any(board[i][column] == value for i in range(9)):
                return True

    grid_idx = [set(range(0, 2 + 1)), set(range(3, 5+1)), set(range(6, 8+1))]
    #Update possible values when removing value from x_coord, y_coord
    #Add to ROWS:
    for col in range(9): # For each column, we need to check whether 
        if not present_in_board(row = x_coord, column = None, value = value, board = board) and possible_values[x_coord][col] is not None:
            possible_values[x_coord][col].append(value)
    #Add to columns:
    for row in range(9):
        if not present_in_board(row = None, column = y_coord, value = value, board = board) and possible_values[row][y_coord] is not None:
            possible_values[row][y_coord].append(value)
    #Add to nearby grid
    grid_x = x_coord//3
    grid_y = y_coord//3
    for grid_row in grid_idx[grid_x]:
        for grid_col in grid_idx[grid_y]:
            if value not in possible_values[grid_row][grid_col] and possible_values[grid_row][grid_col]:
                possible_values[grid_row][grid_col].append(value)


def find_least_empty(possible_values):
    #We want to find the entry with the least possible values
    #possible_values is a 3D integer array.
    least_values_idx: List[Union[None, int]] = [None, None]
    least_values = 100 #Doesn't matter, as long as it's more than 10
    for row in range(9):
        for col in range(9):
            if possible_values[row][col] and len(possible_values[row][col]) < least_values:
                least_values = len(possible_values[row][col])
                least_values_idx[0] = row
                least_values_idx[1] = col
    return least_values_idx

def is_board_filled(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] is None:
                return False
    return True