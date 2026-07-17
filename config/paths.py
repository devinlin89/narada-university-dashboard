# config/paths.py

from pathlib import Path

# Directories

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"

RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
REFERENCE_DATA_DIR = DATA_DIR / "reference"
TODO_DATA_DIR = REFERENCE_DATA_DIR / "todo" 


# Files

RAW_DATA = RAW_DATA_DIR / "raw_export.csv"

STUDENTS_DATA = PROCESSED_DATA_DIR / "students.csv"
INSTITUTIONS_DATA = PROCESSED_DATA_DIR / "institutions.csv"