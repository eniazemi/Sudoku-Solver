import pandas as pd

# to be added :
# file not found error : if path doesn't exist
# check the total number of numbers given.
# check if the numbers are given in correct form. no str char bool
# check if all the numbers are whole int
# read from csv, txt


def read_table(name_of_table):
    df = pd.read_excel(name_of_table + '.xlsx', sheet_name='Sheet1')
    df = df.fillna(0)
    df = df.astype(int)
    matrix = df.to_numpy()
    return matrix


x = read_table("testExcel")
