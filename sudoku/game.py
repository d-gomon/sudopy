from typing import List, Union, Optional

class SudokuBoard():
    def __init__(self):
        self.size = 9 #Maybe replace later to allow for bigger boards
        self.board: List[List[Optional[Union[int, None]]]] = [[None for i in range(self.size)] for j in range(self.size)] #size x size board initialization
        self.solved = False #We check whether the sudoku game is solved

    def print_board(self):
        # Print the top border
        print("+" + "-------+" * 3)

        for i, row in enumerate(self.board):
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

    def get_coordinate(self, prompt: str) -> int:
        while True:
            try:
                value = int(input(prompt))
                if 1 <= value <= self.size:
                    return value
                else:
                    print("Please enter a value between {1} and {self.size}")
            except ValueError:
                print("Invalid input. Please enter a number")

    def get_coordinates(self) -> tuple[int, int, int]:
        row = self.get_coordinate(prompt = "Enter row(1-9): ")
        column = self.get_coordinate(prompt = "Enter column(1-9): ")
        value = self.get_coordinate(prompt = "Enter new value(1-9): ")
        return (row, column, value)            

    def play_round(self): #Extracts input value and assigns it to the board
        coords = self.get_coordinates()
        self.board[coords[0]-1][coords[1]-1] = coords[2]

    def check_board(self): #checks whether the board is VALID
        #Perform row, then column, then grid checks here.
        self.solved = False

