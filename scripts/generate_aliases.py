from pathlib import Path

import pandas as pd
import argparse

from config.paths import (
    PROCESSED_DATA,
    REFERENCE_DIR,
    TODO_DIR,
)

from config.aliases import ALIAS_FILES

# CLI

parser = argparse.ArgumentParser(
    description="Generate TODO alias files from processed data."
)

parser.add_argument(
    "column",
    choices=ALIAS_FILES.keys(),
    help="Column to generate aliases for."
)

args = parser.parse_args()

column = args.column.lower()


# Load Data

df = pd.read_csv(PROCESSED_DATA)

alias_path = REFERENCE_DIR / ALIAS_FILES[column]

if alias_path.exists():
    alias_df = pd.read_csv(alias_path)
    existing_aliases = set(alias_df["alias"].dropna().astype(str))
else:
    existing_aliases = set()


# Find missing aliases

unique_values = (
    df[column]
    .dropna()
    .astype(str)
    .sort_values()
    .unique()
)

missing = sorted(
    value for value in unique_values if value not in existing_aliases
)


# Write TODO file

TODO_DIR.mkdir(parents=True, exist_ok=True)

todo_path = TODO_DIR / f"{column}_aliases_todo.csv"

todo_df = pd.DataFrame({
    "alias": missing,
    "canonical": ""
})

todo_df.to_csv(todo_path, index=False)

print(f"Found {len(missing)} missing aliases.")
print(f"Saved TODO file to:")
print(todo_path)