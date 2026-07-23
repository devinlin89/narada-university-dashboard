import pandas as pd

from aliases.tables import (
    export_alias_table,
    load_alias_table,
    load_todo_table,
)
from aliases.validation import (
    validate_against_alias_table,
    validate_todo,
)
from common.cli import parse_alias_column_args
from common.pipeline import Pipeline
from config.config import TODO_DATA_DIR
from config.logger import get_logger


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


def delete_todo_file(column: str) -> None:
    # Delete the TODO Alias file

    todo_path = TODO_DATA_DIR / f"{column}_aliases_todo.csv"

    if todo_path.exists():
        todo_path.unlink()


class AliasProcessor(Pipeline):
    # Process reviewed aliases into the reference table
    
    logger = get_logger("aliases.pipeline")

    @classmethod
    def execute(cls) -> None:
        logger = cls.logger

        args = parse_alias_column_args(
            "Merge reviewed aliases to the reference table.",
        )
        column = args.column.lower()

        cls.logger.info(
            "Processing '%s' aliases...",
            column,
        )

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