import pandas as pd

from aliases.tables import load_alias_table
from common.data_io import load_students
from common.pipeline import Pipeline
from config.config import TODO_DATA_DIR
from config.logger import get_logger


def load_existing_alias_values(column: str) -> set[str]:
    """Load existing aliases and canonical values for a column.

    Args:
        column (str): Alias table column to load.

    Returns:
        set[str]: Set containing all existing aliases and canonical values.
    """

    alias_df = load_alias_table(column)

    return set(
        pd.concat(
            [alias_df["alias"], alias_df["canonical"]]
        )
        .dropna()
        .astype(str)
    )


def find_missing_aliases(
    df: pd.DataFrame,
    column: str,
    existing_values: set[str],
) -> list[str]:
    """Find values not yet present in the alias table.

    Args:
        df (pd.DataFrame): Processed dataset containing values to check.
        column (str): Column whose values should be checked.
        existing_values (set[str]): Existing aliases and canonical values.

    Returns:
        list[str]: Sorted list of values missing from the alias table.
    """

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
        if value not in existing_values
    )

    return missing_values


def export_todo(column: str, missing: list[str]) -> None:
    """Export missing aliases to a TODO alias table.

    Args:
        column (str): Alias table column associated with the missing values.
        missing (list[str]): Missing alias values to export.
    """

    TODO_DATA_DIR.mkdir(parents=True, exist_ok=True)

    todo_path = TODO_DATA_DIR / f"{column}_aliases_todo.csv"

    todo_df = pd.DataFrame({
        "alias": missing,
        "canonical": ""
    })

    todo_df.to_csv(todo_path, index=False)


class AliasGenerator(Pipeline):
    """Generate TODO alias tables from processed data."""

    logger = get_logger("aliases.generator")

    @classmethod
    def execute(cls, column: str) -> None:
        """Generate a TODO alias table for a column.

        Args:
            column (str): Column whose missing aliases should be identified.
        """

        logger = cls.logger

        column = column.lower()

        logger.info("Loading processed dataset...")
        df = load_students()

        logger.info("Loading existing aliases for %s...", column)
        existing_values = load_existing_alias_values(column)

        logger.info("Finding missing %s aliases...", column)
        missing_aliases = find_missing_aliases(
            df,
            column,
            existing_values,
        )

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