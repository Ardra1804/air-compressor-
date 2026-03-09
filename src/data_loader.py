import pandas as pd 

def load_excel_data(file_path):
    df = pd.read_excel(file_path, sheet_name=None)
    sheets = {}
    for sheet_name, data in df.items():
        sheets[sheet_name] = data
    return sheets 