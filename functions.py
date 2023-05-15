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

# check if sudoku puzzle is valid
def is_valid(board, row, col, num):
    # Check if 'num' is already present in the current row
    if num in board[row] and num != 0:
        return False

    # Check if 'num' is already present in the current column
    for i in range(9):
        if board[i][col] == num and num != 0:
            return False

    # Check if 'num' is already present in the current 3x3 grid
    start_row = 3 * (row // 3)
    start_col = 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num and num != 0:
                return False

    return True

# iterative dfs algorithm implementation
def solve_sudoku_iteration_dfs(board):
    stack = []  # Initialize the stack
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                stack.append((row, col))

    index = 0  # Index to track the current position in the stack

    while index < len(stack):
        row, col = stack[index]
        found_number = False

        for num in range(board[row][col] + 1, 10):
            if is_valid(board, row, col, num):
                board[row][col] = num
                found_number = True
                index += 1
                break

        if not found_number:
            board[row][col] = 0
            index -= 1

            if index < 0:
                return False

    return board




# entry function to iteration dfs algorithm
# returns a matrix of solved sudoku puzzle
def sudoku_solver_iteration_dfs(board):
    # Create a deep copy of the board to keep the original unchanged
    board_copy = copy.deepcopy(board)

    # Solve the Sudoku puzzle
    if solve_sudoku_iteration_dfs(board_copy):
        return board_copy  # Return the solved Sudoku board
    else:
        return None  # If no solution exists


# code below is used to test the result of algorithms using console

# def print_board(board):
#     # Print the Sudoku board
#     for i in range(9):
#         for j in range(9):
#             print(board[i][j], end=" ")
#         print()

# # Sample Sudoku board
# board = [
#     [5, 3, 0, 0, 7, 0, 0, 0, 0],
#     [6, 0, 0, 1, 9, 5, 0, 0, 0],
#     [0, 9, 8, 0, 0, 0, 0, 6, 0],
#     [8, 0, 0, 0, 6, 0, 0, 0, 3],
#     [4, 0, 0, 8, 0, 3, 0, 0, 1],
#     [7, 0, 0, 0, 2, 0, 0, 0, 6],
#     [0, 6, 0, 0, 0, 0, 2, 8, 0],
#     [0, 0, 0, 4, 1, 9, 0, 0, 5],
#     [0, 0, 0, 0, 8, 0, 0, 7, 9]
# ]

# # sample of an invalid sudoku
# unsolvable_sudoku = [
#     [5, 3, 0, 0, 7, 0, 0, 0, 0],
#     [6, 0, 0, 1, 9, 5, 0, 0, 0],
#     [0, 9, 8, 0, 0, 0, 0, 6, 0],
#     [8, 0, 0, 0, 6, 0, 0, 0, 3],
#     [4, 0, 0, 8, 0, 3, 0, 0, 1],
#     [7, 0, 0, 0, 2, 0, 0, 0, 6],
#     [0, 6, 0, 0, 0, 0, 2, 8, 0],
#     [0, 0, 0, 4, 1, 9, 0, 0, 5],
#     [0, 0, 0, 0, 8, 0, 0, 7, 7]  # Note the duplicate '7' in the last row
# ]

# start_time = time.time()  # Start the timer

# # Solve the Sudoku puzzle
# solved_board = sudoku_solver_iteration_dfs(board)

# end_time = time.time()  # Stop the timer
# elapsed_time = end_time - start_time  # Calculate the elapsed time in seconds
# elapsed_time_ms = elapsed_time * 1000  # Convert elapsed time to milliseconds

# if solved_board is not None:
#     print("Sudoku solved:")
#     print_board(solved_board)
#     print("Time taken to solve the Sudoku puzzle: {:.3f} milliseconds".format(elapsed_time_ms))
# else:
#     print("No solution exists for the Sudoku puzzle.")