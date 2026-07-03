# utils/cli.py

import argparse

from config.aliases import ALIAS_FILES


def parse_alias_column_args(description: str) -> argparse.Namespace:
    # Parse command-line arguments

    parser = argparse.ArgumentParser(
        description=description
    )

    parser.add_argument(
        "column",
        choices=ALIAS_FILES.keys(),
        help="Alias table to operate on"
    )

    return parser.parse_args()