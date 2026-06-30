import pandas as pd
from titlecase import titlecase

from config.column_names import (
    COLUMN_MAPPING,
    DROPPED_COLUMNS,
    FREE_RESPONSE_COLUMNS
)

def main():
    # Loads CSV data into Pandas Dataframe
    df = pd.read_csv("data/raw/export_2026_06_26.csv")

    # Renames columns to shorter names and only keeps relevant columns
    df = df.rename(columns=COLUMN_MAPPING)
    df = df.drop(columns=DROPPED_COLUMNS)

    # Replace yes or no inputs with boolean values
    df["within_jabodetabek"] = df["within_jabodetabek"].replace({
        "Yes, it is within Jabodetabek/Greater Jakarta Area": True,
        "No, it is outside of Jabodetabek/Greater Jakarta Area": False
    })

    df["received_scholarship?"] = df["received_scholarship?"].replace({
        "Yes": True,
        "No": False
    })

    # Converts factors entries strings into lists
    df["decision_factors"] = df["decision_factors"].str.split(",")

    # Replaces empty campus values with main
    df["campus"] = df["campus"].fillna("Main").replace({"-": "Main"})
    df["scholarship_description"] = df["scholarship_description"].fillna("")

    for column in FREE_RESPONSE_COLUMNS:
        df[column] = df[column].apply(titlecase).str.strip()


    # Exports cleaned dataframe to CSV
    df.to_csv("data/processed/students.csv", index=False)

if __name__ == "__main__":
    main()

