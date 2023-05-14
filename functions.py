import os
import pandas as pd
import numpy as np
import copy
import time

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



def is_valid(board, row, col, num):
    # Check if 'num' is already present in the current row
    for i in range(9):
        if board[row][i] == num:
            return False

    # Check if 'num' is already present in the current column
    for i in range(9):
        if board[i][col] == num:
            return False

    # Check if 'num' is already present in the current 3x3 grid
    start_row = 3 * (row // 3)
    start_col = 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False

    return True


def find_unassigned_location(board):
    # Find an unassigned location on the board
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return row, col
    return -1, -1  # If no unassigned location is found


def solve_sudoku(board):
    # Find an unassigned location
    row, col = find_unassigned_location(board)

    # If no unassigned location is found, the puzzle is solved
    if row == -1 and col == -1:
        return True

    # Try different numbers in the unassigned location
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num

            # Recursively solve the puzzle
            if solve_sudoku(board):
                return True

            # If the current configuration doesn't lead to a solution,
            # undo the current assignment and try a different number
            board[row][col] = 0

    return False


def print_board(board):
    # Print the Sudoku board
    for i in range(9):
        for j in range(9):
            print(board[i][j], end=" ")
        print()


# Sample Sudoku board (0 represents empty cells)
board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

if solve_sudoku(board):
    print("Sudoku solved:")
    print_board(board)
else:
    print("No solution exists for the")
