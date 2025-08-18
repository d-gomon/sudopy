
def play_game(SudokuBoard):
    #We want the game to wait for user input as long as the sudoku puzzle is not solved
    SudokuBoard.print_board()
    while SudokuBoard.solved == False:
        SudokuBoard.play_round()
        SudokuBoard.print_board()