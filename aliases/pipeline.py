from time import perf_counter

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
from config.config import TODO_DATA_DIR
from config.logger import (
    configure_logging,
    get_logger,
)

logger = get_logger("aliases.pipeline")


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


class AliasProcessor:
    # Run the complete student data cleaning workflow
    
    @staticmethod
    def run() -> None:
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