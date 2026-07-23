from time import perf_counter

import pandas as pd

from aliases.tables import load_alias_table
from common.cli import parse_alias_column_args
from common.data_io import load_students
from config.config import TODO_DATA_DIR
from config.logger import (
    configure_logging,
    get_logger,
)

logger = get_logger("aliases.generator")


def load_existing_aliases(column: str) -> set[str]:
    # Load the existing aliases for the specified column

    alias_df = load_alias_table(column)

    return set(
        alias_df["alias"]
        .dropna()
        .astype(str)
    )


def find_missing_aliases(
        df: pd.DataFrame,
        column: str,
        existing_aliases: set[str]
) -> list[str]:
    # Find values that are not yet present in the alias table

    unique_values = (
        df[column]
        .dropna()
        .astype(str)
        .sort_values()
        .unique()
    )

    missing_values = sorted(
        value 
        for value in unique_values 
        if value not in existing_aliases
    )

    return missing_values


def export_todo(column: str, missing: list[str]) -> None:
    # Export the TODO alias file

    TODO_DATA_DIR.mkdir(parents=True, exist_ok=True)

    todo_path = TODO_DATA_DIR / f"{column}_aliases_todo.csv"

    todo_df = pd.DataFrame({
        "alias": missing,
        "canonical": ""
    })

    todo_df.to_csv(todo_path, index=False)


class AliasGenerator:
    # Generate TODO alias tables from processed data

    @staticmethod
    def run() -> None:
        configure_logging()

        start_time = perf_counter()

        try:
            args = parse_alias_column_args(
                "Generate TODO alias files from processed data.",
            )
            column = args.column.lower()

            logger.info("Loading processed dataset...")
            df = load_students()

            logger.info("Loading existing aliases for %s...", column)
            existing_aliases = load_existing_aliases(column)

            logger.info("Finding missing aliases...")
            missing_aliases = find_missing_aliases(df, column, existing_aliases)

            logger.info("Found %d missing aliases.", len(missing_aliases))

            if missing_aliases:
                logger.info("Exporting TODO alias table...")
                export_todo(column, missing_aliases)

                logger.info(
                    "Exported TODO file to %s",
                    TODO_DATA_DIR / f"{column}_aliases_todo.csv"
                )
            else:
                logger.info("No missing aliases found.")

            logger.info("Alias generation completed successfully.")

        except Exception:
            logger.exception("Alias generation failed.")
            raise

        finally:
            elapsed = perf_counter() - start_time
            logger.info("Total execution time: %.3f s.", elapsed)