import os
import pandas as pd
import numpy as np
import copy
import time
from collections import deque

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


def check_table(path):
    path_valid = check_if_path_valid(path)
    if not path_valid:
        return {"response": "BAD PATH"}

    df = pd.read_excel(path)
    df_temp = df.fillna(0)

    all_chars_numeric = check_if_all_chars_are_numbers(df_temp)

    if not all_chars_numeric:
        return {"response": "ALL THE DATA IN EXCEL SHOULD BE NUMBER"}

    if not is_9x9(df):
        return {"response": "TABLE SHOULD BE IN 9x9 FORMAT"}

    return {"response": "200"}


def solve_table(path, algorithm):
    df = pd.read_excel(path)

    get_total_number_given_from_df(df)
    df = df.fillna(0)
    matrix = df.to_numpy().astype(int)
    total_time = 1
    x = time.time()

    if algorithm == "Backtracking":
        solution = backtracking_solve_sudoku(matrix)
        total_time = time.time() - x
        file_path = r"C:\Users\User\Desktop\Sudoku-Solver\result-Backtracking.xlsx"

    elif algorithm == "Depth Limited Search":
        solution = solve_sudoku_dls(matrix)
        solution = np.vstack(solution[0]).reshape(9, 9)
        total_time = time.time() - x
        file_path = r"C:\Users\User\Desktop\Sudoku-Solver\result-DLS.xlsx"

    elif algorithm == "Breadth First Search":
        solution = solve_sudoku_bfs(matrix)
        total_time = time.time() - x
        file_path = r"C:\Users\User\Desktop\Sudoku-Solver\result-BFS.xlsx"

    elif algorithm == "iteration dfs":
        solution = solve_sudoku_iteration_dfs(matrix)
        total_time = time.time() - x
        file_path = r"C:\Users\User\Desktop\Sudoku-Solver\result-iDFS.xlsx"

    text = "Algorithm: " + algorithm + ". Time used: " + str(total_time) + " seconds. Number given as input: " + str(
        total_number_given)

    new_row = pd.DataFrame([text], columns=["Description"])
    df = pd.DataFrame(solution)
    df = df.append(new_row, ignore_index=True)

    df.to_excel(file_path, index=False)

    return matrix


def solve_sudoku_dls(puzzle, depth_limit=81):
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


def solve_sudoku_bfs(puzzle):
    queue = deque()  # Initialize the queue
    queue.append(puzzle)
    visited = set()  # Track visited states

    while queue:
        current = queue.popleft()

        if is_solved(current):
            return current

        row, col = choose_next_cell(current)

        for num in range(1, 10):
            if is_valid(current, row, col, num):
                new_puzzle = copy.deepcopy(current)
                new_puzzle[row][col] = num

                # Check if the new state has been visited before
                state = tuple(map(tuple, new_puzzle))
                if state not in visited:
                    visited.add(state)
                    queue.append(new_puzzle)

    return None


def backtracking_solve_sudoku(board):
    def is_valid(row, col, num):
        # Check if the number already exists in the row
        for i in range(9):
            if board[row][i] == num:
                return False

        # Check if the number already exists in the column
        for i in range(9):
            if board[i][col] == num:
                return False

        # Check if the number already exists in the 3x3 box
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == num:
                    return False

        return True

    def find_empty_cell():
        # Find the next empty cell (cell with value 0)
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return i, j
        return None

    def solve():
        cell = find_empty_cell()

        # If there are no empty cells, the puzzle is solved
        if cell is None:
            return True

        row, col = cell

        # Try different numbers from 1 to 9
        for num in range(1, 10):
            if is_valid(row, col, num):
                board[row][col] = num

                # Recursively solve the puzzle
                if solve():
                    return True

                # If the current number doesn't lead to a solution, reset the cell
                board[row][col] = 0

        return False

    # Call the solve function to solve the puzzle
    if solve():
        return board
    else:
        return None


def is_valid(board, row, col, num):
    # Check if the number is already present in the row
    for i in range(9):
        if board[row][i] == num:
            return False

    # Check if the number is already present in the column
    for i in range(9):
        if board[i][col] == num:
            return False

    # Check if the number is already present in the 3x3 grid
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False

    return True
