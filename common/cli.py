import argparse

from config.config import ALIAS_FILE_NAMES


def parse_alias_column_args(description: str) -> argparse.Namespace:
    # Parse command-line arguments

    parser = argparse.ArgumentParser(description=description)

    ALIAS_COLUMNS = ALIAS_FILE_NAMES.keys()

    parser.add_argument(
        "column", choices=ALIAS_COLUMNS, help="Alias table to operate on"
    )

    return parser.parse_args()