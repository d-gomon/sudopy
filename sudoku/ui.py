def get_coordinate(prompt: str, SudokuBoard) -> int:
    while True:
        try:
            value = int(input(prompt))
            if 1 < value <= SudokuBoard.size:
                return value
            else:
                print("Please enter a value between {1} and {SudokuBoard.size}")
        except ValueError:
            print("Invalid input. Please enter a number")



def get_coordinates(SudokuBoard) -> tuple:
    row = get_coordinate("Enter row(1-9): ", SudokuBoard = SudokuBoard)
    column = get_coordinate("Enter column(1-9): ", SudokuBoard = SudokuBoard)
    value = get_coordinate("Enter new value(1-9): ", SudokuBoard = SudokuBoard)
    return (row, column, value)


def play_game(SudokuBoard):
    #We want the game to wait for user input as long as the sudoku puzzle is not solved
    while SudokuBoard.solved == False:
        coords = get_coordinates(SudokuBoard = SudokuBoard)
        coord_value = SudokuBoard.board[coords[0]][coords[1]]
        SudokuBoard.board[coords[0]][coords[1]] = coords[2]