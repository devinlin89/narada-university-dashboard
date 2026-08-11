import pandas as pd

from common.exceptions import ValidationError


def validate_todo(todo_df: pd.DataFrame) -> None:
    """Validate a TODO alias table before applying it.

    Args:
        todo_df (pd.DataFrame): The TODO alias table to validate.

    Raises:
        ValidationError: If validation fails.
    """

    for column in ("alias", "canonical"):
        # Check for missing values
        missing = [
            row + 2
            for row in todo_df.index[todo_df[column].isna()]
        ]

        if missing:
            raise ValidationError(
                f"TODO file contains blank {column} values "
                f"on CSV rows: {missing}"
            )

        # Check for empty strings
        empty = [
            row + 2
            for row in todo_df.index[
                todo_df[column].str.strip() == ""
            ]
        ]

        if empty:
            raise ValidationError(
                f"TODO file contains empty {column} values "
                f"on CSV rows: {empty}"
            )

    # Duplicate aliases
    duplicates = todo_df["alias"][
        todo_df["alias"].duplicated(keep=False)
    ].unique()

    if len(duplicates) > 0:
        raise ValidationError(
            "TODO file contains duplicate aliases: "
            + ", ".join(sorted(duplicates))
        )


def validate_against_alias_table(
    alias_df: pd.DataFrame,
    todo_df: pd.DataFrame,
) -> None:
    """Ensure TODO aliases do not already exist.

    Args:
        alias_df (pd.DataFrame): The existing alias table.
        todo_df (pd.DataFrame): The TODO alias table to validate.

    Raises:
        ValidationError: If one or more aliases already exist.
    """

    existing = set(alias_df["alias"].astype(str))

    conflicts = sorted(
        set(todo_df["alias"].astype(str)) & existing
    )

    if conflicts:
        raise ValidationError(
            "The following aliases already exist in the alias table: "
            + ", ".join(conflicts)
        )