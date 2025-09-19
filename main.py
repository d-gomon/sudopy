from sudoku.game import SudokuBoard
from sudoku.makegame import start_game
from sudoku.ui import chooseGameType
from sudoku.exceptions import BackToMainMenu
import curses



def main():
    while True: #Keep looping through games. Never shut down
        try:
            CurrentGame = SudokuBoard()
            chooseGameType(CurrentGame)
            start_game(CurrentGame)
        except BackToMainMenu:
            continue


main()