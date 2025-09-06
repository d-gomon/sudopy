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
            for col in range(9):
                if possible_values[x_coord][col] and value in possible_values[x_coord][col]:
                    possible_values[x_coord][col].remove(value)
                    any_change = True
            #Remove from COLUMNS:
            for row in range(9):
                if possible_values[row][y_coord] and value in possible_values[row][y_coord]:
                    possible_values[row][y_coord].remove(value)
                    any_change = True
            #Remove from nearby grid:
            grid_x = x_coord//3
            grid_y = y_coord//3
            for grid_row in grid_idx[grid_x]:
                for grid_col in grid_idx[grid_y]:
                    if possible_values[grid_row][grid_col] is not None and value in possible_values[grid_row][grid_col]:
                        possible_values[grid_row][grid_col].remove(value)
                        any_change = True
    #At the end, return whether we actually changed anything
    #If we haven't changed anything anymore, we might need to use some more serious logic
    return any_change