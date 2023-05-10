import pandas as pd

df = pd.read_excel('testExcel.xlsx', sheet_name='Sheet1')
df = df.fillna(0)
matrix = df.to_numpy()
