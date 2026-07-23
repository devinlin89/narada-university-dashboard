# utils/alias.py

import pandas as pd

from common.data_io import load_csv_or_empty
from config.config import (
    ALIAS_FILES,
    ALIASES_DIR,
    TODO_DATA_DIR,
)


def load_alias_table(column: str) -> pd.DataFrame:
    # Load the alias table for the specified column.

    return load_csv_or_empty(
        ALIASES_DIR / ALIAS_FILES[column],
        ["alias", "canonical"],
    )


def load_todo_table(column: str) -> pd.DataFrame:
    # Load the TODO alias table for the specified column.

    return load_csv_or_empty(
        TODO_DATA_DIR / f"{column}_aliases_todo.csv",
        ["alias", "canonical"],
    )


def load_institution_names() -> set[str]:
    # Load every institution alias and canonical name

    alias_df = load_alias_table("institution")

    names = set(alias_df["alias"].dropna().astype(str))
    names.update(alias_df["canonical"].dropna().astype(str))

    return names


def load_alias_mapping(column: str) -> dict[str, str]:
    # Load an alias to canonical mapping

    alias_df = load_alias_table(column)

    return dict(
        zip(
            alias_df["alias"],
            alias_df["canonical"],
            strict=True
        )
    )


def apply_alias_table(
        series: pd.Series,
        column: str
) -> pd.Series:
    # Replace aliases with canonical values

    mapping = load_alias_mapping(column)

    return series.replace(mapping)


def get_aliases(column: str, name: str) -> list[str]:
    # Get all aliases for a given canonical name

    alias_df = load_alias_table(column)

    return alias_df.loc[
        alias_df["canonical"] == name,
        "alias"
    ].dropna().astype(str).tolist()