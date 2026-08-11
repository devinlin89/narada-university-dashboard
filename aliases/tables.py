import pandas as pd

from common.data_io import load_csv_or_empty
from config.config import (
    ALIAS_FILE_NAMES,
    ALIASES_DIR,
    TODO_DATA_DIR,
)


def load_alias_table(column: str) -> pd.DataFrame:
    """Load the alias table for the specified column.

    Args:
        column(str): Column key used to look up the alias file name.

    Returns:
        pd.DataFrame: Alias DataFrame containing columns "alias" and "canonical".
    """

    return load_csv_or_empty(
        ALIASES_DIR / ALIAS_FILE_NAMES[column],
        ["alias", "canonical"],
    )


def load_todo_table(column: str) -> pd.DataFrame:
    """Load the TODO alias table for the specified column.

    Args:
        column (str): Column key used to look up the TODO file name.

    Returns:
        pd.DataFrame: TODO DataFrame containing columns "alias" and "canonical".
    """

    return load_csv_or_empty(
        TODO_DATA_DIR / f"{column}_aliases_todo.csv",
        ["alias", "canonical"],
    )


def load_institution_names() -> set[str]:
    """Load all institution aliases and canonical names.

    Returns:
        set[str]: Set containing every alias and canonical institution name.
    """

    alias_df = load_alias_table("institution")

    names = set(alias_df["alias"].dropna().astype(str))
    names.update(alias_df["canonical"].dropna().astype(str))

    return names


type AliasMapping = dict[str, str]


def load_alias_mapping(column: str) -> AliasMapping:
    """Load an alias-to-canonical mapping for a column.

    Args:
        column (str): Alias table column to load.

    Returns:
        AliasMapping: Dictionary mapping aliases to their canonical values.
    """

    alias_df = load_alias_table(column)

    return dict(zip(alias_df["alias"], alias_df["canonical"], strict=True))


def apply_alias_table(series: pd.Series, column: str) -> pd.Series:
    """Replace aliases in a Series with their canonical values.

    Args:
        series (pd.Series): Series containing aliases to replace.
        column (str): Alias table column to use for the replacements.

    Returns:
        pd.Series: Series with aliases replaced by their canonical values.
    """

    mapping = load_alias_mapping(column)

    return series.replace(mapping)


def get_aliases(column: str, name: str) -> list[str]:
    """Get all aliases associated with a canonical name.

    Args:
        column (str): Alias table column to search.
        name (str): Canonical name whose aliases should be returned.

    Returns:
        list[str]: List of aliases associated with the canonical name.
    """

    alias_df = load_alias_table(column)

    return (
        alias_df.loc[alias_df["canonical"] == name, "alias"]
        .dropna()
        .astype(str)
        .tolist()
    )


def export_alias_table(alias_df: pd.DataFrame, column: str) -> None:
    """Export an alias table to its corresponding CSV file.

    Args:
        alias_df (pd.DataFrame): Alias table to export.
        column (str): Alias table column determining the output file.
    """

    alias_path = ALIASES_DIR / ALIAS_FILE_NAMES[column]

    alias_path.parent.mkdir(parents=True, exist_ok=True)
    alias_df.to_csv(alias_path, index=False)