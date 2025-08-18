class SudokuBoard():
    def __init__():
        self.size = 9 #Maybe replace later to allow for bigger boards
        self.board = [[0 for i in range(size)] for j in range(size)] #size x size board initialization
        self.solved = False #We check whether the sudoku game is solved

    def print_board(self): #printing function to visualize current sudoku board
        for row in self.board:
            print(" ".join(str(col)) for col in row)


