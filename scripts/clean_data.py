from pathlib import Path

import pandas as pd
from titlecase import titlecase

from config.column_names import (
    COLUMN_MAPPING,
    DROPPED_COLUMNS,
    FREE_RESPONSE_COLUMNS,
    LIST_RESPONSE_COLUMNS
)

from config.replacements import (
    VALUE_MAPPINGS,
    DEFAULT_VALUES
)


# Path Configurations

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DATA = PROJECT_ROOT / "data" / "raw" / "export_2026_06_26.csv"
PROCESSED_DATA = PROJECT_ROOT / "data" / "processed" / "students.csv"


# Pipeline Stages

def load_data() -> pd.DataFrame:
    # Load the raw Google Forms export into a Pandas df
    return pd.read_csv(RAW_DATA)


def apply_schema(df: pd.DataFrame) -> pd.DataFrame:
    # Rename columns and remove unused columns

    df = df.rename(columns=COLUMN_MAPPING)
    df = df.drop(columns=DROPPED_COLUMNS)

    return df


def normalize_values(df: pd.DataFrame) -> pd.DataFrame:
    # Apply configured value mappings

    for column, mapping in VALUE_MAPPINGS.items():
        df[column] = df[column].replace(mapping)

    return df


def normalize_lists(df: pd.DataFrame) -> pd.DataFrame:
    # Convert comma-separated response strings into Python lists

    for column in LIST_RESPONSE_COLUMNS:
        df[column] = df[column].str.split(", ")

    return df


def apply_defaults(df: pd.DataFrame) -> pd.DataFrame:
    # Apply default values

    for column, default in DEFAULT_VALUES.items():
        df[column] = (
            df[column]
            .fillna(default)
            .replace({"-": default})
        )

    return df


def normalize_text(df: pd.DataFrame) -> pd.DataFrame:
    # Standardize free-response text

    for column in FREE_RESPONSE_COLUMNS:
        df[column] = (
            df[column]
            .str.strip()
            .apply(lambda x: titlecase(x.strip())
                   if isinstance(x, str) else x)
        )

    return df


def export_data(df: pd.DataFrame) -> None:
    # Save the cleaned dataset CSV file

    PROCESSED_DATA.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_DATA, index=False)


# Main Function

def main() -> None:
    df = load_data()

    df = apply_schema(df)
    df = normalize_values(df)
    df = normalize_lists(df)
    df = apply_defaults(df)
    df = normalize_text(df)

    export_data(df)


if __name__ == "__main__":
    main()

'''hello
'''