import argparse

import pandas as pd

from config.aliases import ALIAS_FILES

from config.logger import (
    configure_logging,
    get_logger,
)

from config.paths import (
    PROCESSED_DATA,
    REFERENCE_DIR,
    TODO_DIR,
)

logger = get_logger("scripts.generate_aliases")


def parse_args() -> argparse.Namespace:
    # Parse command-line arguments

    parser = argparse.ArgumentParser(
        description="Generate TODO alias files from processed data."
    )

    parser.add_argument(
        "column",
        choices=ALIAS_FILES.keys(),
        help="Column to generate aliases for."
    )

    return parser.parse_args()


def load_students() -> pd.DataFrame:
    # Load the processed student dataset

    return pd.read_csv(PROCESSED_DATA)


def load_existing_aliases(column: str) -> set[str]:
    # Load the existing aliases for the specified column

    alias_path = REFERENCE_DIR / ALIAS_FILES[column]

    if not alias_path.exists():
        return set()

    alias_df = pd.read_csv(alias_path)

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
        value for value in unique_values if value not in existing_aliases
    )

    return missing_values


def export_todo(column: str, missing: list[str]) -> None:
    # Export the TODO alias file

    TODO_DIR.mkdir(parents=True, exist_ok=True)

    todo_path = TODO_DIR / f"{column}_aliases_todo.csv"

    todo_df = pd.DataFrame({
        "alias": missing,
        "canonical": ""
    })

    todo_df.to_csv(todo_path, index=False)


# Main Function

def main() -> None:
    configure_logging()

    try:
        args = parse_args()
        column = args.column.lower()

        logger.info("Loading processed dataset...")
        df = load_students()

        logger.info("Loading existing aliases for %s...", column)
        existing_aliases = load_existing_aliases(column)

        logger.info("Finding missing aliases...")
        missing_aliases = find_missing_aliases(df, column, existing_aliases)

        logger.info("Found %d missing aliases.", len(missing_aliases))

        export_todo(column, missing_aliases)

        logger.info("Exported TODO file to %s", TODO_DIR / f"{column}_aliases_todo.csv")
        logger.info("Alias generation completed successfully.")

    except Exception:
        logger.exception("Alias generation failed.")
        raise

if __name__ == "__main__":
    main()