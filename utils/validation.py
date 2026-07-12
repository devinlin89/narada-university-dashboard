# utils/validation.py

import pandas as pd

from config.aliases import ALIAS_FILES
from config.column_names import (
    BOOLEAN_COLUMNS,
    LIST_RESPONSE_COLUMNS,
    REQUIRED_COLUMNS,
)
from utils.alias import load_alias_table


def validate_required_fields(df: pd.DataFrame) -> None:
    # Ensure all required fields contain non-empty values

    for column in REQUIRED_COLUMNS:
        missing = df[column].isna() | (
            df[column]
            .astype(str)
            .str.strip()
            .eq("")
        )

        if missing.any():
            rows = (missing[missing].index + 2).tolist()

            raise ValueError(
                f"Required field '{column}' contains missing "
                f"values on CSV rows: {rows}"
            )


def validate_column_type(
    df: pd.DataFrame,
    columns: tuple[str, ...] | list[str],
    expected_type: type,
) -> None:
    # Ensure all non-null values in the specified columns have the expected type

    for column in columns:
        invalid = df[column].dropna().apply(
            lambda value: not isinstance(value, expected_type)
        )

        if invalid.any():
            rows = (invalid[invalid].index + 2).tolist()

            raise TypeError(
                f"Column '{column}' contains invalid "
                f"{expected_type.__name__} values on CSV rows: {rows}"
            )


def validate_boolean_columns(df: pd.DataFrame) -> None:
    validate_column_type(
        df,
        BOOLEAN_COLUMNS,
        bool,
    )


def validate_list_columns(df: pd.DataFrame) -> None:
    validate_column_type(
        df,
        LIST_RESPONSE_COLUMNS,
        list,
    )


def validate_aliases(df: pd.DataFrame) -> None:
    # Ensure no unresolved aliases remain in the cleaned dataset

    for column in ALIAS_FILES:
        alias_df = load_alias_table(column)

        unresolved_aliases = set(
            alias_df.loc[
                alias_df["alias"] != alias_df["canonical"],
                "alias",
            ]
            .dropna()
            .astype(str)
        )

        remaining = sorted(
            set(df[column].dropna().astype(str))
            & unresolved_aliases
        )

        if remaining:
            raise ValueError(
                f"Column '{column}' still contains unresolved aliases: "
                f"{', '.join(remaining)}"
            )