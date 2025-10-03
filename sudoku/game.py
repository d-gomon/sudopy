from typing import List, Union, Optional
from sudoku.exceptions import BackToMainMenu
import curses

class SudokuBoard():
    def __init__(self):
        self.size = 9 #Maybe replace later to allow for bigger boards
        self.board: List[List[Optional[Union[int, None]]]] = [[None for i in range(self.size)] for j in range(self.size)] #size x size board initialization
        self.solved = False #We check whether the sudoku game is solved
        self.gametype: Union[None, int] = None #Gametypes: 1 - normal sudoku, 2 - solve sudoku, 3 - generate sudoku

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

    def input_board(self, stdscr):
        """Allows the user to input a Sudoku board using arrow keys, WASD, and number pad."""
        stdscr.clear()
        stdscr.keypad(True)
        stdscr.addstr(0, 0, "Use arrow keys or WASD to move, number keys to input, '0' to clear, 'q' to quit.")
        stdscr.addstr(1, 0, "Press 'Enter' to confirm your board.")
        row, col = 0, 0  # Current cursor position

        while True:
            # Draw the board with 3x3 grid separation
            stdscr.clear()
            stdscr.addstr(0, 0, "Use arrow keys or WASD to move, number keys to input, '0' to clear, 'q' to quit.")

            # Draw horizontal lines for 3x3 grid separation
            for i in range(self.size + 1):
                if i % 3 == 0 and i != 0:
                    stdscr.addstr(i + 1, 1, "-" * (self.size * 2 + 1))

            for i in range(self.size):
                for j in range(self.size):
                    value = self.board[i][j]
                    x = j * 2 + 2
                    y = i + 2
                    if i == row and j == col:
                        stdscr.addstr(y, x, str(value) if value is not None else " ", curses.A_REVERSE)
                    else:
                        stdscr.addstr(y, x, str(value) if value is not None else " ")
                    # Draw vertical lines for 3x3 grid separation
                    if (j + 1) % 3 == 0 and j != self.size - 1:
                        stdscr.addstr(y, x + 1, "|")

            # Refresh the screen
            stdscr.refresh()

            # Get user input
            key = stdscr.getch()
            stdscr.keypad(True)

            # Handle arrow keys and WASD
            if key in (curses.KEY_UP, ord('w')) and row > 0:
                row -= 1
            elif key in (curses.KEY_DOWN, ord('s')) and row < self.size - 1:
                row += 1
            elif key in (curses.KEY_LEFT, ord('a')) and col > 0:
                col -= 1
            elif key in (curses.KEY_RIGHT, ord('d')) and col < self.size - 1:
                col += 1
            # Handle number input (1-9)
            elif 49 <= key <= 57:  # ASCII for '1' to '9'
                self.board[row][col] = key - 48  # Convert ASCII to int
            # Handle '0' to clear the cell
            elif key == 48:  # ASCII for '0'
                self.board[row][col] = None
            # Handle 'q' to quit
            elif key == ord('q'):
                return
            # Handle 'Enter' to confirm
            elif key == 10:  # ASCII for Enter
                return



    def get_coordinate(self, prompt: str) -> int:
        while True:
            try:
                value = input(prompt)
                if value == 'q':
                    raise BackToMainMenu
                value = int(value)
                if 1 <= value <= self.size:
                    return value
                else:
                    print("Please enter a value between {1} and {self.size}")
            except ValueError:
                print("Invalid input. Please enter a number")

    def get_coordinates(self) -> tuple[int, int, int]:
        row = self.get_coordinate(prompt = "Enter row(1-9): or q to quit")
        column = self.get_coordinate(prompt = "Enter column(1-9): or q to quit")
        value = self.get_coordinate(prompt = "Enter new value(1-9): or q to quit")
        return (row, column, value)            

    def play_round(self): #Extracts input value and assigns it to the board
        coords = self.get_coordinates()
        self.board[coords[0]-1][coords[1]-1] = coords[2]

    def check_board(self): #checks whether the board is VALID
        #Perform row, then column, then grid checks here.
        
        self.solved = False
    
    def is_board_filled(self):
        for row in range(9):
            for col in range(9):
                if self.board[row][col] is None:
                    return False
        return True

