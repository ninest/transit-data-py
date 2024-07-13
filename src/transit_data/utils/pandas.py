import pandas as pd


def notNaN(val):
    return None if pd.isna(val) else val
