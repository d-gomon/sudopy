from collections import Counter

#Here we program the solver logic.
#When we are solving, we only get the board as input, and the possible values we have determined up until now


def solve_row_column_grid(board, possible_values) -> bool:
    #Input: a sudoku board
    #Side effect: updated possible_values, using information in board
    #Output: did we change anything in the possible values?

    grid_idx = [set(range(0, 2 + 1)), set(range(3, 5+1)), set(range(6, 8+1))]

    #Let's keep track if we actually changed anything
    any_change: bool = False

    #We go through the values of the board, and at each point we update the row/col/grid
    for x_coord in range(9):
        for y_coord in range(9):
            value = board[x_coord][y_coord]
            #First set possible_values to only that value where there already is a value
            if value:
                possible_values[x_coord][y_coord] = [value]
            
            #Remove from ROWS:
            for col in range(9):
                if possible_values[x_coord][col] and col is not y_coord and value in possible_values[x_coord][col]:
                    possible_values[x_coord][col].remove(value)
                    any_change = True
            
            #Remove from COLUMNS:
            for row in range(9):
                if possible_values[row][y_coord] and row is not x_coord and value in possible_values[row][y_coord]:
                    possible_values[row][y_coord].remove(value)
                    any_change = True
            
            #Remove from nearby grid:
            grid_x = x_coord//3
            grid_y = y_coord//3
            for grid_row in grid_idx[grid_x]:
                for grid_col in grid_idx[grid_y]:
                    if possible_values[grid_row][grid_col] is not None and grid_row is not x_coord and grid_col is not y_coord and value in possible_values[grid_row][grid_col]:
                        possible_values[grid_row][grid_col].remove(value)
                        any_change = True
        
    #At the end, return whether we actually changed anything
    #If we haven't changed anything anymore, we might need to use some more serious logic
    return any_change


def solve_secondary_row(board, possible_values):
    #Sometimes it's not sufficient to solve a sudoku game simply by checking row/col/grid logic
    #Sometimes you need to additionally check whether within a grid there is a row/col 
    #That MUST contain a certain value. This allows you to remove this value from the 
    #corresponding row in the adjacent grids as well.
    
    #Logic for this is: Go through grids (1,1), (1, 2), (1,3), (2,1), ..., (3,3) and check for this situation
    #If this situation is present for some number: For all grids with the same row/col number, 
    #remove the value from possible_values in the corresponding row

    grid_idx = [set(range(0, 2 + 1)), set(range(3, 5+1)), set(range(6, 8+1))]
    any_change = False

    #-------------Find a grid where a certain value is ONLY possible in a row or column------
    for grid_x in range(3):
        for grid_y in range(3):
            for value in range(1, 10):
                possible_positions = []
                for row in grid_idx[grid_x]:
                    for col in grid_idx[grid_y]:
                        if possible_values[row][col] and value in possible_values[row][col]:
                            possible_positions.append((row, col))
            # Check if all possible positions are in the same row
                rows = set(pos[0] for pos in possible_positions)
                if len(rows) == 1:
                    row = rows.pop()
                    # Remove 'value' from the rest of the row, outside this grid
                    for c in range(9):
                        if c not in grid_idx[grid_y] and possible_values[row][c] and value in possible_values[row][c]:
                            possible_values[row][c].remove(value)
                            any_change = True

                # Check if all possible positions are in the same column
                cols = set(pos[1] for pos in possible_positions)
                if len(cols) == 1:
                    col = cols.pop()
                    # Remove 'value' from the rest of the column, outside this grid
                    for r in range(9):
                        if r not in grid_idx[grid_x] and possible_values[r][col] and value in possible_values[r][col]:
                            possible_values[r][col].remove(value)
                            any_change = True
    #Did we make any change by using this logic?
    return any_change

def check_grids(board, possible_values):
    #In each grid, we want to check which unique numbers are still possible. 
    #If a number is only possible in one of the empty coordinates, it must be there

    
    grid_idx = [set(range(0, 2 + 1)), set(range(3, 5+1)), set(range(6, 8+1))]
    grid_idx_slice = [slice(0, 2 + 1), slice(3, 5+1), slice(6, 8+1)]
    any_change = False

    for grid_x in range(3):
        for grid_y in range(3):
            #possible_numbers = set(board[grid_idx[grid_x]][grid_idx[grid_y]])
            #Which unique numbers are still possible in each grid (and not taken up in board yet)?
            #breakpoint()
            already_filled_numbers = {num for row in board[grid_idx_slice[grid_x]] for num in row[grid_idx_slice[grid_y]]}
            already_filled_numbers.discard(None)
            grid_unique_numbers = {x for x in range(1,10) if x not in already_filled_numbers}
            grid_possible_numbers = [num for row in possible_values[grid_idx_slice[grid_x]] for num in row[grid_idx_slice[grid_y]]]
            flattened = [num for sublist in grid_possible_numbers for num in sublist if num in grid_unique_numbers]
            counts = Counter(flattened)
            unique_numbers = [num for num, count in counts.items() if count == 1]
            if unique_numbers:
                for unique_num in unique_numbers:
                    for x_coord in grid_idx[grid_x]:
                        for y_coord in grid_idx[grid_y]:
                            if board[x_coord][y_coord] is None and unique_num in possible_values[x_coord][y_coord]:
                                possible_values[x_coord][y_coord] = [unique_num]
                                any_change = True
    #Did we change anything by running this function?
    return any_change


            


def fill_unique_possibilities(board, possible_values):
    #Fill board with the unique possible values in possible_values
    for x_coord in range(9):
        for y_coord in range(9):
            if possible_values[x_coord][y_coord] and len(possible_values[x_coord][y_coord]) == 1:
                value = possible_values[x_coord][y_coord].pop()
                board[x_coord][y_coord] = value

def solve_board_internal(SudokuBoard):
    #We want to apply our solving logic repeatedly until the board is full
    #First we check whether the simple logic can make any change, if so, keep repeating
    #If the simple logic (row/col/grid) cannot, then attempt the harder logic, circle back to see if now simpler logic works again
    #At each step, we need to check if any of the possible_value entries contain 1 entry, and put that entry into the board!
    #Finally, once the full board is filled, we want to stop.

    possible_values = [[list(range(1, SudokuBoard.size + 1)) for i in range(SudokuBoard.size)] for j in range(SudokuBoard.size)]  

    while SudokuBoard.solved == False:
        progress_made = False
        while solve_row_column_grid(SudokuBoard.board, possible_values=possible_values):
            fill_unique_possibilities(SudokuBoard.board, possible_values=possible_values)
            print("simple logic1")
            progress_made = True
        while solve_secondary_row(SudokuBoard.board, possible_values=possible_values):
            fill_unique_possibilities(SudokuBoard.board, possible_values=possible_values)
            print("Secondary logic")
            progress_made = True
        while check_grids(SudokuBoard.board, possible_values=possible_values):
            breakpoint()
            fill_unique_possibilities(SudokuBoard.board, possible_values=possible_values)
            print("grid logic")
            progress_made = True
        if SudokuBoard.is_board_filled():
            SudokuBoard.solved = True
        if not progress_made:
            print("Could not solve this sudoku! Either too hard or not enough info! Printing final board:")
            break
        SudokuBoard.print_board()