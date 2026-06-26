import pandas as pd

df = pd.read_csv("data/raw/export_2026_06_26.csv")

print(df.head())
print(df.columns)
print(df.info())