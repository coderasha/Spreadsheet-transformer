import pandas as pd


def read_excel(file_path):
    if file_path.endswith(".csv"):
        return pd.read_csv(file_path)

    return pd.read_excel(file_path)