
def chooseGameType(SudokuBoard) -> bool:
    #We can choose either of the 3 game types:
    #1. Play a Sudoku Game (requires additional parameter after: difficulty)
    #2. Solve a manually inputted sudoku board
    #3. Generate Sudoku Board (not really a game)
    while True:
            try:
                value = int(input("What would you like to do?\n"
                "1. Play Sudoku Game\n"
                "2. Solve a Sudoku Game (manual board input)\n"
                "3. Generate a valid Sudoku Board\n"
                "4. Quit\n"))
                if 1 <= value <= 4:
                    SudokuBoard.gametype = value
                    return True
                else:
                    print("Please enter a value between {1} and {3}")
            except ValueError:
                print("Invalid input. Please enter a number between {1} and {3}")
    

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
