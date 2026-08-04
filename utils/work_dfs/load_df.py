import pandas as pd

def simple_load_df(raw_file):
    if raw_file.endswith('.parquet'):
        return pd.read_parquet(raw_file)
    return pd.read_csv(raw_file)