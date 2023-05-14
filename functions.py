import os
import pandas as pd
import numpy as np

total_number_given = 0


def get_total_number_given_from_df(df):
    numeric_cols = df.select_dtypes(include=np.number).columns

    global total_number_given
    total_number_given = df[numeric_cols].count().sum()


def check_if_path_valid(path):
    if os.path.exists(path):
        return True
    return False


def check_if_all_chars_are_numbers(df):
    try:
        df = df.replace([np.nan, -np.nan], np.nan).fillna(0).astype(int)
        df.astype(int)
        return True
    except ValueError:
        return False


def is_9x9(df):
    shape = df.shape
    if shape[0] == 9 and shape[1] == 9:
        return True
    return False


def read_table(path):
    path_valid = check_if_path_valid(path)
    if not path_valid:
        return {"error_code": "BAD PATH"}

    df = pd.read_excel(path)
    df_temp = df.fillna(0)

    all_chars_numeric = check_if_all_chars_are_numbers(df_temp)

    if not all_chars_numeric:
        return {"error_code": "ALL THE DATA IN EXCEL SHOULD BE NUMBER"}

    if not is_9x9(df):
        return {"error_code": "TABLE SHOULD BE IN 9x9 FORMAT"}

    get_total_number_given_from_df(df)
    df = df.fillna(0)
    matrix = df.to_numpy().astype(int)
    # print(matrix)
    return matrix


 
def solve_sudoku_dls(puzzle, depth_limit):
    # Create a copy of the puzzle to avoid modifying the original
    puzzle_copy = [row[:] for row in puzzle]
    
    return s_helper_dls(puzzle_copy, depth_limit)
    

def s_helper_dls(puzzle, depth_limit):
    # If the puzzle is solved, return it
    if is_solved(puzzle):
        return puzzle, depth_limit

    # If the depth limit has been reached, return None
    if depth_limit == 0:
        return None

    # Choose the next empty cell to fill
    row, col = choose_next_cell(puzzle)

    # Try each valid value for the cell recursively
    for val in range(1, 10):
        if is_valid(puzzle, row, col, val):
            puzzle[row][col] = val
            result = s_helper_dls(puzzle, depth_limit - 1)
            if result is not None:
                # A solution was found
                return result
            puzzle[row][col] = 0

    # No solution found within the depth limit
    return None

 # Check if all cells are filled
def is_solved(puzzle):
    for row in range(9):
        for col in range(9):
            if puzzle[row][col] == 0:
                return False
    return True

 # Choose the next empty cell with the fewest possible values
def choose_next_cell(puzzle):
    min_count = 10
    next_cell = None
    for row in range(9):
        for col in range(9):
            if puzzle[row][col] == 0:
                count = count_possible_values(puzzle, row, col)
                if count < min_count:
                    min_count = count
                    next_cell = (row, col)
    return next_cell

 # Count the number of possible values for a cell
def count_possible_values(puzzle, row, col):
   
    values = set(range(1, 10))
    for i in range(9):
        values.discard(puzzle[row][i])
        values.discard(puzzle[i][col])
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            values.discard(puzzle[i][j])
    return len(values)

# Check if a value is valid for a cell
def is_valid(puzzle, row, col, val):
    
    for i in range(9):
        if puzzle[row][i] == val or puzzle[i][col] == val:
            return False
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if puzzle[i][j] == val:
                return False
    return True
