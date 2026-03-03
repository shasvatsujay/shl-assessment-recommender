import pandas as pd

file_path ='Gen_AI Dataset.xlsx'

xls = pd.ExcelFile(file_path)

print("Sheets in file:", xls.sheet_names)

for sheet in xls.sheet_names:
    df = pd.read_excel(xls, sheet_name=sheet)
    print("\nSheet:", sheet)
    print(df.head())