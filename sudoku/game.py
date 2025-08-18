class SudokuBoard():
    def __init__(self):
        self.size = 9 #Maybe replace later to allow for bigger boards
        self.board = [[0 for i in range(self.size)] for j in range(self.size)] #size x size board initialization
        self.solved = False #We check whether the sudoku game is solved

    def print_board(self): #printing function to visualize current sudoku board
        for row in self.board:
            print(" ".join(str(col) for col in row))
    
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

    def get_coordinates(self) -> tuple:
        row = self.get_coordinate(prompt = "Enter row(1-9): ")
        column = self.get_coordinate(prompt = "Enter column(1-9): ")
        value = self.get_coordinate(prompt = "Enter new value(1-9): ")
        return (row, column, value)            

    def play_round(self): #Extracts input value and assigns it to the board
        coords = self.get_coordinates()
        self.board[coords[0]-1][coords[1]-1] = coords[2]

