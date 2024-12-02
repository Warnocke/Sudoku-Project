import math,random
import pygame

"""
This was adapted from a GeeksforGeeks article "Program for Sudoku Generator" by Aarti_Rathi and Ankur Trisal
https://www.geeksforgeeks.org/program-sudoku-generator/

"""

class SudokuGenerator:
    """
	create a sudoku board - initialize class variables and set up the 2D board
	This should initialize:
	self.row_length		- the length of each row
	self.removed_cells	- the total number of cells to be removed
	self.board			- a 2D list of ints to represent the board
	self.box_length		- the square root of row_length

	Parameters:
    row_length is the number of rows/columns of the board (always 9 for this project)
    removed_cells is an integer value - the number of cells to be removed

	Return:
	None
    """""

    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.box_length = int(row_length ** 0.5)
        self.board = []
        for i in range(row_length):
            self.board.append([])
            for j in range(row_length):
                self.board[i].append("_")
    '''
	Returns a 2D python list of numbers which represents the board

	Parameters: None
	Return: list[list]
    '''
    def get_board(self):
        return self.board
    '''
	Displays the board to the console
    This is not strictly required, but it may be useful for debugging purposes

	Parameters: None
	Return: None
    '''
    def print_board(self):
        pass

    '''
	Determines if num is contained in the specified row (horizontal) of the board
    If num is already in the specified row, return False. Otherwise, return True

	Parameters:
	row is the index of the row we are checking
	num is the value we are looking for in the row
	
	Return: boolean
    '''
    def valid_in_row(self, row, num):
        pass

    '''
	Determines if num is contained in the specified column (vertical) of the board
    If num is already in the specified col, return False. Otherwise, return True

	Parameters:
	col is the index of the column we are checking
	num is the value we are looking for in the column
	
	Return: boolean
    '''
    def valid_in_col(self, col, num):
        pass

    '''
	Determines if num is contained in the 3x3 box specified on the board
    If num is in the specified box starting at (row_start, col_start), return False.
    Otherwise, return True

	Parameters:
	row_start and col_start are the starting indices of the box to check
	i.e. the box is from (row_start, col_start) to (row_start+2, col_start+2)
	num is the value we are looking for in the box

	Return: boolean
    '''
    def valid_in_box(self, row_start, col_start, num):
        pass
    
    '''
    Determines if it is valid to enter num at (row, col) in the board
    This is done by checking that num is unused in the appropriate, row, column, and box

	Parameters:
	row and col are the row index and col index of the cell to check in the board
	num is the value to test if it is safe to enter in this cell

	Return: boolean
    '''
    def is_valid(self, row, col, num):
        pass

    '''
    Fills the specified 3x3 box with values
    For each position, generates a random digit which has not yet been used in the box

	Parameters:
	row_start and col_start are the starting indices of the box to check
	i.e. the box is from (row_start, col_start) to (row_start+2, col_start+2)

	Return: None
    '''
    def fill_box(self, row_start, col_start):
        pass
    
    '''
    Fills the three boxes along the main diagonal of the board
    These are the boxes which start at (0,0), (3,3), and (6,6)

	Parameters: None
	Return: None
    '''
    def fill_diagonal(self):
        pass

    '''
    DO NOT CHANGE
    Provided for students
    Fills the remaining cells of the board
    Should be called after the diagonal boxes have been filled
	
	Parameters:
	row, col specify the coordinates of the first empty (0) cell

	Return:
	boolean (whether or not we could solve the board)
    '''
    def fill_remaining(self, row, col):
        if (col >= self.row_length and row < self.row_length - 1):
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row // self.box_length * self.box_length):
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True
        
        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    '''
    DO NOT CHANGE
    Provided for students
    Constructs a solution by calling fill_diagonal and fill_remaining

	Parameters: None
	Return: None
    '''
    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, self.box_length)

    '''
    Removes the appropriate number of cells from the board
    This is done by setting some values to 0
    Should be called after the entire solution has been constructed
    i.e. after fill_values has been called
    
    NOTE: Be careful not to 'remove' the same cell multiple times
    i.e. if a cell is already 0, it cannot be removed again

	Parameters: None
	Return: None
    '''
    def remove_cells(self):
        pass


class Board():
    """
    Represents the entire Sudoku board, which is a 9x9 grid made of Cell objects.
    """""

    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        # self.grid = need cell class
        # self.selected_cell = need cell class

    def draw(self):
        """
        Draws the Sudoku grid and all the cells on the screen.
        - Draws the grid outline with bold lines for 3x3 boxes.
        - Calls the draw method of each cell to display its value or sketch.
        """""
        for i in range(self.width+1):
            pygame.draw.line(self.screen, "black", (80 * i, 0), (80 * i, 720), 3)
        for i in range(self.height+1):
            pygame.draw.line(self.screen, "black", (0, 80 * i), (720, 80 * i), 3)


        for i in range(1, self.width//3):
            pygame.draw.line(self.screen, "black", (80 * i * (self.width//3), 0), (80 * i * (self.width//3), 720), 6)
        for i in range(1, self.height//3):
            pygame.draw.line(self.screen, "black", (0, 80 * i * (self.width//3)), (720, 80 * i * (self.width//3)), 6)

    def select(self, row, col):
        """
        Marks the cell at (row, col) as the currently selected cell.
        - Highlights the selected cell.
        """""
        pass

    def click(self, x, y):
        """
        Determines if a click (x, y) is inside the grid.
        - If so, returns the (row, col) of the clicked cell.
        - If not, returns None.
        """""
        pass

    def clear(self):
        """
        Clears the value or sketched value of the selected cell.
        - Only works on cells the user is allowed to edit.
        """""
        pass

    def sketch(self, value):
        """
        Sets a sketched value in the top-left corner of the selected cell.
        - Sketched values are temporary and can be changed later.
        """""
        pass

    def place_number(self, value):
        """
        Sets the final value of the selected cell.
        - The sketched value is cleared after the final value is placed.
        """""
        pass

    def reset_to_original(self):
        """
        Resets the board to its original state.
        - Clears all user-filled cells, keeping only the initial values.
        """""
        pass

    def is_full(self):
        """
        Checks if the board is completely filled (no empty cells).
        - Returns True if full, False otherwise.
        """""
        pass

    def update_board(self):
        """
        Updates the 2D grid based on the current values of all Cell objects.
        """""
        pass

    def find_empty(self):
        """"
        Finds an empty cell on the board.
        - Returns the (row, col) of the first empty cell found.
        - If no empty cells remain, returns None.
        """""
        pass

    def check_board(self):
        """"
        Checks if the current state of the board satisfies the Sudoku rules:
        - Each row contains unique values.
        - Each column contains unique values.
        - Each 3x3 box contains unique values.

        Returns True if the board is valid and solved, False otherwise.
        """""
        pass


'''
DO NOT CHANGE
Provided for students
Given a number of rows and number of cells to remove, this function:
1. creates a SudokuGenerator
2. fills its values and saves this as the solved state
3. removes the appropriate number of cells
4. returns the representative 2D Python Lists of the board and solution

Parameters:
size is the number of rows/columns of the board (9 for this project)
removed is the number of cells to clear (set to 0)

Return: list[list] (a 2D Python list to represent the board)
'''
def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    board = sudoku.get_board()
    sudoku.remove_cells()
    board = sudoku.get_board()
    return board

def main():
    try:
        pygame.init()

        screen_width, screen_height = 720, 720
        screen = pygame.display.set_mode((screen_width, screen_height))
        clock = pygame.time.Clock()
        sudoku_board = generate_sudoku(9, 0)

        difficulty = "easy"
        board = Board(width=9, height=9, screen=screen, difficulty=difficulty)

        running = True
        while running:

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print("click")

                if event.type == pygame.QUIT:
                    running = False

            screen.fill("light blue")
            screen.blit(pygame.image.load("sam classroom.png"), pygame.image.load("sam classroom.png").get_rect(topleft=(0, 0)))
            board.draw()

            pygame.display.flip()
            clock.tick(60)

    finally:
        pygame.quit()

if __name__ == "__main__":
    main()