import math, random
import pygame
from pygame.examples.moveit import WIDTH, HEIGHT
# from matplotlib.pyplot import fill_between

"""
This was adapted from a GeeksforGeeks article "Program for Sudoku Generator" by Aarti_Rathi and Ankur Trisal
https://www.geeksforgeeks.org/program-sudoku-generator/

"""


class Cell:
    def __init__(self, value, row, col, screen, cell_size=60, is_generated=False):

        self.value = value
        self.row = row
        self.col = col
        self.sketched_value = 0
        self.screen = screen
        self.cell_size = cell_size
        self.selected = False
        self.is_generated = is_generated

    def set_cell_value(self, value):
        if not self.is_generated:
            self.value = value

    def set_sketched_value(self, value):
        if not self.is_generated:
            self.sketched_value = value

    def draw(self):

        x = self.row * self.cell_size
        y = self.col * self.cell_size

        # Draw the cell border
        border_color = (255, 0, 0) if self.selected else (0, 0, 0)
        pygame.draw.rect(self.screen, border_color, (x, y, self.cell_size, self.cell_size), 2)
        font = pygame.font.Font(None, 60)
        if self.value != 0:
            textColor = (255, 117, 117)
            if self.is_generated:
                textColor = (54, 54, 54)
            text = font.render(str(self.value), True, textColor)
            self.screen.blit(text, (-4 + x + self.cell_size // 3, -5 + y + self.cell_size // 3))
        elif self.sketched_value != 0:

            text = font.render(str(self.sketched_value), True, (128, 128, 128))
            self.screen.blit(text, (x + self.cell_size // 3, y + self.cell_size // 3))


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

    def print_board(self):
        for row in self.board:
            print(" ".join(str(cell) if cell != 0 else "." for cell in row))

    '''
	Determines if num is contained in the specified row (horizontal) of the board
    If num is already in the specified row, return False. Otherwise, return True

	Parameters:
	row is the index of the row we are checking
	num is the value we are looking for in the row

	Return: boolean
    '''

    def valid_in_row(self, row, num):
        return num not in self.board[row]

    '''
	Determines if num is contained in the specified column (vertical) of the board
    If num is already in the specified col, return False. Otherwise, return True

	Parameters:
	col is the index of the column we are checking
	num is the value we are looking for in the column

	Return: boolean
    '''

    def valid_in_col(self, col, num):
        return num not in [self.board[row][col] for row in range(self.row_length)]

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
        for row in range(row_start, row_start + 3):
            for col in range(col_start, col_start + 3):
                if self.board[row][col] == num:
                    return False
        return True

    '''
    Determines if it is valid to enter num at (row, col) in the board
    This is done by checking that num is unused in the appropriate, row, column, and box

	Parameters:
	row and col are the row index and col index of the cell to check in the board
	num is the value to test if it is safe to enter in this cell

	Return: boolean
    '''

    def is_valid(self, row, col, num):
        if not self.valid_in_row(row, num):
            return False
        if not self.valid_in_col(col, num):
            return False
        box_row_start = (row // 3) * 3
        col_row_start = (col // 3) * 3
        if not self.valid_in_box(box_row_start, col_row_start, num):
            return False
        return True

    '''
    Fills the specified 3x3 box with values
    For each position, generates a random digit which has not yet been used in the box

	Parameters:
	row_start and col_start are the starting indices of the box to check
	i.e. the box is from (row_start, col_start) to (row_start+2, col_start+2)

	Return: None
    '''

    def fill_box(self, row_start, col_start):
        for row in range(row_start, row_start + 3):
            for col in range(col_start, col_start + 3):
                while self.board[row][col] == '_':
                    new_num = random.randint(1, 9)
                    if self.valid_in_box(row_start, col_start, new_num):
                        self.board[row][col] = new_num

    '''
    Fills the three boxes along the main diagonal of the board
    These are the boxes which start at (0,0), (3,3), and (6,6)

	Parameters: None
	Return: None
    '''

    def fill_diagonal(self):
        for i in range(0, 7, 3):
            self.fill_box(i, i)

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
        removed = 0
        while removed < self.removed_cells:
            row = random.randrange(self.row_length)
            col = random.randrange(self.row_length)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                removed += 1


class Board():
    """
    Represents the entire Sudoku board, which is a 9x9 grid made of Cell objects.
    """""

    def __init__(self, width, height, screen, difficulty, sudoku_board):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.grid = [
            [
                Cell(
                    value=sudoku_board[row][col],
                    row=row,
                    col=col,
                    screen=screen,
                    cell_size=60,
                    is_generated=(sudoku_board[row][col] != 0),
                )
                for col in range(width)
            ]
            for row in range(height)
        ]
        self.selected_cell = None

    def draw(self):
        """
        Draws the Sudoku grid and all the cells on the screen.
        - Draws the grid outline with bold lines for 3x3 boxes.
        - Calls the draw method of each cell to display its value or sketch.
        """""
        cell_size = 60
        scale = 0.75
        for i in range(1, self.width // 3):
            pygame.draw.line(self.screen, "black", (60 * i * (self.width // 3), 0), (60 * i * (self.width // 3), 720*scale),6)
        for i in range(1, self.height // 3):
            pygame.draw.line(self.screen, "black", (0, 60 * i * (self.width // 3)), (720*scale, 60 * i * (self.width // 3)),6)

        for row in self.grid:
            for cell in row:
                cell.draw()

    def select(self, row, col):
        """
        Marks the cell at (row, col) as the currently selected cell.
        - Highlights the selected cell.
        """""
        if self.selected_cell:
            prev_row, prev_col = self.selected_cell
            self.grid[prev_row][prev_col].selected = False

        self.selected_cell = (row, col)
        self.grid[row][col].selected = True

    def click(self, x, y):
        """
        Determines if a click (x, y) is inside the grid.
        - If so, returns the (row, col) of the clicked cell.
        - If not, returns None.
        """""
        grid = (540, 540)
        cell_size = grid[0] // 9
        if x < grid[0] and y < grid[1]:
            row = x // cell_size
            col = y // cell_size
            self.select(row, col)
            return row, col
        return None

    def clear(self):
        """
        Clears the value or sketched value of the selected cell.
        - Only works on cells the user is allowed to edit.
        """""
        if self.selected_cell:
            row, col = self.selected_cell
            if not self.grid[row][col].is_generated:
                self.grid[row][col].set_cell_value(0)
                self.grid[row][col].set_sketched_value(0)

    def sketch(self, value):
        """
        Sets a sketched value in the top-left corner of the selected cell.
        - Sketched values are temporary and can be changed later.
        """""
        if self.selected_cell:
            row, col = self.selected_cell
            self.grid[row][col].set_sketched_value(value)

    def place_number(self, value):
        """
        Sets the final value of the selected cell.
        - The sketched value is cleared after the final value is placed.
        """""
        if self.selected_cell:
            row, col = self.selected_cell
            if not self.grid[row][col].is_generated:
                self.grid[row][col].set_cell_value(value)
                self.grid[row][col].set_sketched_value(0)

    def reset_to_original(self, original_board):
        """
        Resets the board to its original state.
        - Clears all user-filled cells, keeping only the initial values.
        """""
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                self.grid[row][col].set_cell_value(original_board[row][col])
                self.grid[row][col].set_sketched_value(0)
                self.grid[row][col].selected = False

    def is_full(self):
        """
        Checks if the board is completely filled (no empty cells).
        - Returns True if full, False otherwise.
        """""
        for row in self.grid:
            for cell in row:
                if cell.value == 0:
                    return False
        return True

    def update_board(self):
        """
        Updates the 2D grid based on the current values of all Cell objects.
        """""
        return [[cell.value for cell in row] for row in self.grid]

    def find_empty(self):
        """"
        Finds an empty cell on the board.
        - Returns the (row, col) of the first empty cell found.
        - If no empty cells remain, returns None.
        """""
        for i in range(9):
            for j in range(9):
                if self.grid[i][j].value == 0:
                    return (i, j)
        return None

    def check_board(self):
        """"
        Checks if the current state of the board satisfies the Sudoku rules:
        - Each row contains unique values.
        - Each column contains unique values.
        - Each 3x3 box contains unique values.

        Returns True if the board is valid and solved, False otherwise.
        """""
        # Check all rows
        for row in range(9):
            if not self.is_unique([self.grid[row][col].value for col in range(9)]):
                return False

        # Check all columns
        for col in range(9):
            if not self.is_unique([self.grid[row][col].value for row in range(9)]):
                return False

        # Check all 3x3 boxes
        for row_start in range(0, 9, 3):
            for col_start in range(0, 9, 3):
                box_values = [self.grid[row][col].value for row in range(row_start, row_start + 3) for col in
                              range(col_start, col_start + 3)]
                if not self.is_unique(box_values):
                    return False

        return True  # Board is valid

    # Helper function to check uniqueness, excluding zeros (empty cells)
    def is_unique(self, values):
        numbers = [value for value in values if value != 0]
        return len(numbers) == len(set(numbers))


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
        scale = 0.75
        screen_width, screen_height = 720*scale, 800*scale
        screen = pygame.display.set_mode((screen_width, screen_height))
        clock = pygame.time.Clock()

        start_screen = True

        easy_button = pygame.Rect(screen_width // 3, screen_height // 2, screen_width // 3, 50)
        medium_button = pygame.Rect(screen_width // 3, screen_height // 2 + 100, screen_width // 3, 50)
        hard_button = pygame.Rect(screen_width // 3, screen_height // 2 + 200, screen_width // 3, 50)

        while start_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    start_screen = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if easy_button.collidepoint(event.pos):
                        difficulty = "easy"
                        original_board = generate_sudoku(9, 30)
                        print("easy")
                        start_screen = False
                    elif medium_button.collidepoint(event.pos):
                        difficulty = "medium"
                        original_board = generate_sudoku(9,40)
                        print("medium")
                        start_screen = False
                    elif hard_button.collidepoint(event.pos):
                        difficulty = "hard"
                        original_board = generate_sudoku(9,50)
                        print("hard")
                        start_screen = False

            screen.fill((71, 78, 79))
            title_font = pygame.font.Font(None, 80)
            button_font = pygame.font.Font(None, 50)

            title_text = title_font.render("Sudoku Game", True, "black")
            title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 3))
            screen.blit(title_text, title_rect)

            pygame.draw.rect(screen, "black", easy_button)
            pygame.draw.rect(screen, "black", medium_button)
            pygame.draw.rect(screen, "black", hard_button)

            easy_text = button_font.render("Easy", True, "white")
            medium_text = button_font.render("Medium", True, "white")
            hard_text = button_font.render("Hard", True, "white")

            easy_text_rect = easy_text.get_rect(center=easy_button.center)
            medium_text_rect = medium_text.get_rect(center=medium_button.center)
            hard_text_rect = hard_text.get_rect(center=hard_button.center)

            screen.blit(easy_text, easy_text_rect)
            screen.blit(medium_text, medium_text_rect)
            screen.blit(hard_text, hard_text_rect)

            b = pygame.image.load("Sudoku Background.png")
            screen.blit(b,b.get_rect(topleft=(0, 0)))

            pygame.display.flip()
            clock.tick(60)

        board = Board(width=9, height=9, screen=screen, difficulty="easy", sudoku_board=original_board)

        for row in range(len(original_board)):
            for col in range(len(original_board[row])):
                board.grid[row][col].set_cell_value(original_board[row][col])

        restart_button = pygame.Rect(50*scale, 740*scale, 180*scale, 40*scale)
        reset_button = pygame.Rect(270*scale, 740*scale, 180*scale, 40*scale)
        exit_button = pygame.Rect(490*scale, 740*scale, 180*scale, 40*scale)

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button.collidepoint(event.pos):
                        print("restart button")
                        start_screen = True
                        break
                    elif reset_button.collidepoint(event.pos):
                        board.reset_to_original(original_board)
                        print("reset button")
                    elif exit_button.collidepoint(event.pos):
                        running = False
                        print("exit button")

                    cellPosition = board.click(event.pos[0], event.pos[1])
                    # if cellPosition is not None:
                    #     # print(f'clicked in cell: {cellPosition}, value: {board.grid[cellPosition[0]][cellPosition[1]].value}')
                    #     # print(original_board)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        board.place_number(0)
                    if event.key in range(pygame.K_1, pygame.K_9 + 1):
                        num = event.key - pygame.K_0
                        if board.selected_cell:
                            board.place_number(num)

                if event.type == pygame.QUIT:
                    running = False

            screen.fill((237, 245, 255))
            s = pygame.image.load("sam pixel classroom scaled.png")
            s.set_alpha(60)
            screen.blit(s,s.get_rect(topleft=(0, 0)))
            board.draw()

            pygame.draw.rect(screen, "black", restart_button)
            pygame.draw.rect(screen, "black", reset_button)
            pygame.draw.rect(screen, "black", exit_button)

            button_font = pygame.font.Font(None, 40)

            restart_text = button_font.render("Restart", 0, "white")
            reset_text = button_font.render("Reset", 0, "white")
            exit_text = button_font.render("Exit", 0, "white")

            restart_rect = restart_text.get_rect(center=restart_button.center)
            reset_rect = reset_text.get_rect(center=reset_button.center)
            exit_rect = exit_text.get_rect(center=exit_button.center)

            screen.blit(restart_text, restart_rect)
            screen.blit(reset_text, reset_rect)
            screen.blit(exit_text, exit_rect)

            if board.is_full():
                if board.check_board():
                    font = pygame.font.Font(None, 80)
                    win_text = font.render("Game Won!", True, "black")
                    win_rect = win_text.get_rect(center=(screen_width // 2, screen_height // 3))
                    screen.fill("light blue")
                    screen.blit(win_text, win_rect)

                    exit_button = pygame.Rect(screen_width // 3, screen_height // 1.5, 200 * scale, 50 * scale)
                    pygame.draw.rect(screen, "black", exit_button)
                    button_font = pygame.font.Font(None, 40)
                    exit_text = button_font.render("Exit", 0, "white")
                    exit_rect = exit_text.get_rect(center=exit_button.center)
                    screen.blit(exit_text, exit_rect)
                else:
                    font = pygame.font.Font(None, 80)
                    over_text = font.render("Game Over :(", True, "black")
                    over_rect = over_text.get_rect(center=(screen_width // 2, screen_height // 3))
                    screen.fill("light blue")
                    screen.blit(over_text, over_rect)

                    restart_button = pygame.Rect(screen_width // 3, screen_height // 1.5, 200 * scale, 50 * scale)
                    pygame.draw.rect(screen, "black", restart_button)
                    button_font = pygame.font.Font(None, 40)
                    restart_text = button_font.render("Restart", 0, "white")
                    restart_rect = restart_text.get_rect(center=restart_button.center)
                    screen.blit(restart_text, restart_rect)

            pygame.display.flip()
            clock.tick(60)

            if start_screen:
                main()

    finally:
        pygame.quit()


if __name__ == "__main__":
    main()