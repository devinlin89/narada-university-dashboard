import pandas as pd


def validate_todo(todo_df: pd.DataFrame) -> None:
    # Validate a TODO alias table before applying it.

    for column in ("alias", "canonical"):
        # Check for missing values
        missing = [
            row + 2
            for row in todo_df.index[todo_df[column].isna()]
        ]

        if missing:
            raise ValueError(
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
            raise ValueError(
                f"TODO file contains empty {column} values "
                f"on CSV rows: {empty}"
            )

    # Duplicate aliases
    duplicates = todo_df["alias"][
        todo_df["alias"].duplicated(keep=False)
    ].unique()

    if len(duplicates) > 0:
        raise ValueError(
            "TODO file contains duplicate aliases: "
            + ", ".join(sorted(duplicates))
        )


def validate_against_alias_table(
    alias_df: pd.DataFrame,
    todo_df: pd.DataFrame,
) -> None:
    # Ensure TODO aliases do not already exist.

    existing = set(alias_df["alias"].astype(str))

    conflicts = sorted(
        set(todo_df["alias"].astype(str)) & existing
    )

    if conflicts:
        raise ValueError(
            "The following aliases already exist in the alias table: "
            + ", ".join(conflicts)
        )