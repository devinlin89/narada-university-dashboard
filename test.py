import pandas as pd

from config.column_names import COLUMN_MAPPING
from config.column_names import DROPPED_COLUMNS

df = pd.read_csv("data/raw/export_2026_06_26.csv")

df = df.rename(columns = COLUMN_MAPPING)

df = df.drop(columns=DROPPED_COLUMNS)

print(df.columns)
