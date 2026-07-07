# utils/alias.py

from pathlib import Path

import pandas as pd

from config.aliases import ALIAS_FILES
from config.paths import (
    REFERENCE_DIR,
    TODO_DIR,
)


def load_csv_or_empty(path: Path, columns: list[str]) -> pd.DataFrame:
    # Load a CSV file or return an empty DataFrame if it does not exist.

    if not path.exists():
        return pd.DataFrame(columns=columns)

    return pd.read_csv(path)


def load_alias_table(column: str) -> pd.DataFrame:
    # Load the alias table for the specified column.

    return load_csv_or_empty(
        REFERENCE_DIR / ALIAS_FILES[column],
        ["alias", "canonical"],
    )


def load_todo_table(column: str) -> pd.DataFrame:
    # Load the TODO alias table for the specified column.

    return load_csv_or_empty(
        TODO_DIR / f"{column}_aliases_todo.csv",
        ["alias", "canonical"],
    )


def load_institution_names() -> set[str]:
    """Load every institution alias and canonical name."""

    alias_df = load_alias_table("institution")

    names = set(alias_df["alias"].dropna().astype(str))
    names.update(alias_df["canonical"].dropna().astype(str))

    return names