import argparse

from config.config import ALIAS_FILE_NAMES


def parse_alias_column_args(description: str) -> argparse.Namespace:
    """Parse command-line arguments for selecting an alias table.

    Args:
        description (str): Description displayed by the command-line argument
            parser.

    Returns:
        argparse.Namespace: Parsed command-line arguments containing the
            selected alias table.
    """

    parser = argparse.ArgumentParser(description=description)

    ALIAS_COLUMNS = ALIAS_FILE_NAMES.keys()

    parser.add_argument(
        "column", choices=ALIAS_COLUMNS, help="Alias table to operate on"
    )

    return parser.parse_args()