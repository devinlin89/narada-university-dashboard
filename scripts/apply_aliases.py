from time import perf_counter

import pandas as pd

from utils.cli import parse_alias_column_args
from utils.alias import (
    load_alias_table,
    load_todo_table,
)
from config.aliases import ALIAS_FILES
from config.logger import (
    configure_logging,
    get_logger,
)
from config.paths import (
    REFERENCE_DIR,
    TODO_DIR,
)

logger = get_logger("scripts.apply_aliases")


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


def merge_aliases(
    alias_df: pd.DataFrame,
    todo_df: pd.DataFrame
) -> pd.DataFrame:
    # Merge the existing alias DataFrame with the validated TODO alias Dataframe

    return (
        pd.concat(
            [alias_df, todo_df],
            ignore_index=True
        )
        .sort_values(by="alias")
        .reset_index(drop=True)
    )


def export_alias_table(alias_df: pd.DataFrame, column: str) -> None:
    # Export the updated alias table

    alias_path = REFERENCE_DIR / ALIAS_FILES[column]

    alias_path.parent.mkdir(parents=True, exist_ok=True)
    alias_df.to_csv(alias_path, index=False)


def delete_todo_file(column: str) -> None:
    # Delete the TODO Alias file

    todo_path = TODO_DIR / f"{column}_aliases_todo.csv"

    if todo_path.exists():
        todo_path.unlink()


def main() -> None:
    configure_logging()

    start_time = perf_counter()

    try:
        args = parse_alias_column_args(
            "Merge reviewed aliases to the reference table.",
        )
        column = args.column.lower()

        logger.info("Loading alias table...")
        alias_df = load_alias_table(column)
        logger.info("Loading TODO alias table...")
        todo_df = load_todo_table(column)

        logger.info("Validating TODO alias table...")
        validate_todo(todo_df)
        validate_against_alias_table(alias_df, todo_df)

        logger.info("Merging alias tables...")
        alias_df = merge_aliases(alias_df, todo_df)

        logger.info("Alias table now contains %d aliases.", len(alias_df))

        logger.info("Exporting updated alias table...")
        export_alias_table(alias_df, column)

        logger.info("Deleting TODO file...")
        delete_todo_file(column)

        logger.info("Alias application completed successfully.")

    except Exception:
        logger.exception("Alias application failed.")
        raise

    finally:
        elapsed = perf_counter() - start_time
        logger.info("Total execution time: %.3f s.", elapsed)

if __name__ == "__main__":
    main()