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



def solve_sudoku(board):
    stack = [(board, 0, 0)]
    while stack:
        curr_board, row, col = stack.pop()
        if row == 9:
            return curr_board
        if curr_board[row][col] != 0:
            if col == 8:
                stack.append((curr_board, row+1, 0))
            else:
                stack.append((curr_board, row, col+1))
            continue
        for num in range(1, 10):
            if is_valid(curr_board, row, col, num):
                curr_board[row][col] = num
                if col == 8:
                    stack.append((curr_board, row+1, 0))
                else:
                    stack.append((curr_board, row, col+1))
        curr_board[row][col] = 0
    return None


def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num:
            return False
        if board[i][col] == num:
            return False
        if board[3*(row//3) + i//3][3*(col//3) + i%3] == num:
            return False
    return True
