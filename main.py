from sudoku.game import SudokuBoard
from sudoku.ui import play_game
from sudoku.makegame import createValidBoard


CurrentGame = SudokuBoard()
createValidBoard(CurrentGame)
play_game(CurrentGame)



