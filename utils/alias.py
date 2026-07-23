# utils/alias.py

from pathlib import Path

import pandas as pd

from config.config import (
    ALIAS_FILES,
    ALIASES_DIR,
    TODO_DATA_DIR,
)


def load_csv_or_empty(path: Path, columns: list[str]) -> pd.DataFrame:
    # Load a CSV file or return an empty DataFrame if it does not exist.

    if not path.exists():
        return pd.DataFrame(columns=columns)

    return pd.read_csv(path)


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
    """Load every institution alias and canonical name."""

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