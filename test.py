import pandas as pd
from titlecase import titlecase

from config.column_names import COLUMN_MAPPING
from config.column_names import DROPPED_COLUMNS

df = pd.read_csv("data/raw/export_2026_06_26.csv")

df = df.rename(columns=COLUMN_MAPPING)

df = df.drop(columns=DROPPED_COLUMNS)

print(df.columns)


df["within_jabodetabek"] = df["within_jabodetabek"].replace({
    "Yes, it is within Jabodetabek/Greater Jakarta Area": True,
    "No, it is outside of Jabodetabek/Greater Jakarta Area": False
})

df["received_scholarship?"] = df["received_scholarship?"].replace({
    "Yes": True,
    "No": False
})

df["decision_factors"] = df["decision_factors"].str.split(",")

df["campus"] = df["campus"].fillna("Main").replace({"-": "Main"})

columns_to_capitalize = ["institution", "campus", "city", "major"]

for column in columns_to_capitalize:
    df[column] = df[column].apply(titlecase)



df.to_csv("data/processed/output_2026_06_26.csv", index=False)