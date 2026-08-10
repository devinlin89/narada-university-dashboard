from aliases.pipeline import AliasProcessor
from config.config import (
    ALIAS_COLUMNS,
    TODO_DATA_DIR,
)
from config.logger import get_logger

logger = get_logger("scripts.apply_aliases")


def find_todo_files() -> list[str]:
    """Find alias columns with TODO files."""
    return [
        column
        for column in ALIAS_COLUMNS
        if (TODO_DATA_DIR / f"{column}_aliases_todo.csv").exists()
    ]


def main() -> None:
    """Apply all reviewed alias TODO files."""
    todo_columns = find_todo_files()

    if not todo_columns:
        logger.info("No TODO alias files found.")
        return

    for column in todo_columns:
        AliasProcessor.run(column)


if __name__ == "__main__":
    main()