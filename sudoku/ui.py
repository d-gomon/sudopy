
def play_game(SudokuBoard):
    #We want the game to wait for user input as long as the sudoku puzzle is not solved
    while SudokuBoard.solved == False:
        SudokuBoard.print_board()
        SudokuBoard.play_round()
        



def print_board(board):
    # Print the top border
    print("+" + "-------+" * 3)

    for i, row in enumerate(board):
        # Print row separator after every 3 rows
        if i > 0 and i % 3 == 0:
            print("+" + "-------+" * 3)

        # Print row content
        print("|", end=" ")
        for j, col in enumerate(row):
            print(col if col != None else ".", end=" ")
            # Print vertical separator after every 3 columns
            if (j + 1) % 3 == 0 and j < 8:
                print("|", end=" ")
        print("|")

    # Print the bottom border
    print("+" + "-------+" * 3)