# config/paths.py

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DATA = PROJECT_ROOT / "data" / "raw" / "raw_export.csv"
PROCESSED_DATA = PROJECT_ROOT / "data" / "processed" / "students.csv"

REFERENCE_DIR = PROJECT_ROOT / "data" / "reference"
TODO_DIR = REFERENCE_DIR / "todo"