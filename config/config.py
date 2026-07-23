from pathlib import Path
from types import SimpleNamespace

import yaml

# Helper functions

def _load_yaml(path: Path) -> dict:
    # Load a YAML file

    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _to_namespace(obj):
    # Recursively convert dictionaries to SimpleNamespace
    
    if isinstance(obj, dict):
        return SimpleNamespace(
            **{k: _to_namespace(v) for k, v in obj.items()}
        )
    if isinstance(obj, list):
        return [_to_namespace(v) for v in obj]
    return obj


# Load settings

_CONFIG_PATH = Path(__file__).with_name("settings.yaml")

settings = _to_namespace(
    _load_yaml(_CONFIG_PATH)
)

# Paths

# Project Root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Directories
DATA_DIR = PROJECT_ROOT / settings.paths.data

RAW_DATA_DIR = DATA_DIR / settings.paths.raw
PROCESSED_DATA_DIR = DATA_DIR / settings.paths.processed
REFERENCE_DATA_DIR = DATA_DIR / settings.paths.reference
TODO_DATA_DIR = REFERENCE_DATA_DIR / settings.paths.todo


# Files
RAW_DATA = RAW_DATA_DIR / settings.files.raw_export

STUDENTS_DATA = PROCESSED_DATA_DIR / settings.files.students
INSTITUTIONS_DATA = PROCESSED_DATA_DIR / settings.files.institutions
COORDINATES_DATA = REFERENCE_DATA_DIR / settings.files.coordinates

ALIAS_FILES = vars(settings.aliases)

# Reference data
GEOCODING_OVERRIDES = _load_yaml(
    REFERENCE_DATA_DIR / "geocoding" / "overrides.yaml"
)

_REPLACEMENTS = _load_yaml(
    REFERENCE_DATA_DIR / "mappings" / "replacements.yaml"
)

VALUE_MAPPINGS = _REPLACEMENTS["value_mappings"]
DEFAULT_VALUES = _REPLACEMENTS["default_values"]
MAJOR_TO_ACADEMIC_FIELD = _REPLACEMENTS["major_to_academic_field"]