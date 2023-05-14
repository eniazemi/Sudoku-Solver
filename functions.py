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


def solve_sudoku_iteration_dfs(board):
    stack = [(board, 0, 0)]  # Initialize the stack with the initial state
    while stack:
        curr_board, row, col = stack.pop()
        if row == 9:  # If all rows are filled, the puzzle is solved
            return True
        
        if curr_board[row][col] != 0:
            # Move to the next cell
            next_row = row + 1 if col == 8 else row
            next_col = (col + 1) % 9
            stack.append((curr_board, next_row, next_col))
            continue

        for num in range(1, 10):
            if is_valid(curr_board, row, col, num):
                curr_board[row][col] = num
                # Create a new copy of the board and push it to the stack
                new_board = [row[:] for row in curr_board]
                stack.append((new_board, row, col))
                next_row = row + 1 if col == 8 else row
                next_col = (col + 1) % 9
                stack.append((curr_board, next_row, next_col))
                break

        if not stack:  # If the stack becomes empty, it means there is no solution
            return False

    return False



def sudoku_solver_iteration_dfs(board):
    # Create a deep copy of the board to keep the original unchanged
    board_copy = [row[:] for row in board]

    # Solve the Sudoku puzzle
    if solve_sudoku_iteration_dfs(board_copy):
        return board_copy  # Return the solved Sudoku board
    else:
        return None  # If no solution exists


# Sample sudoku to evaluate the solution and time taken for each algorithm

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

start_time = time.time()  # Start the timer

# Solve the Sudoku puzzle
solved_board = sudoku_solver_iteration_dfs(board)

end_time = time.time()  # Stop the timer
elapsed_time = end_time - start_time  # Calculate the elapsed time in seconds
elapsed_time_ms = elapsed_time * 1000  # Convert elapsed time to milliseconds

if solved_board is not None:
    print("Sudoku solved:")
    print_board(solved_board)
    print("Time taken to solve the Sudoku puzzle: {:.3f} milliseconds".format(elapsed_time_ms))
else:
    print("No solution exists for the Sudoku puzzle.")