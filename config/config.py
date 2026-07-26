from dataclasses import dataclass
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

ALIASES_DIR = REFERENCE_DATA_DIR / "aliases"
GEOCODING_DIR = REFERENCE_DATA_DIR / "geocoding"
MAPPINGS_DIR = REFERENCE_DATA_DIR / "mappings"
TODO_DATA_DIR = REFERENCE_DATA_DIR / "todo"

# Files
RAW_DATA = RAW_DATA_DIR / settings.files.raw_export

STUDENTS_DATA = PROCESSED_DATA_DIR / settings.files.students
INSTITUTIONS_DATA = PROCESSED_DATA_DIR / settings.files.institutions
COORDINATES_DATA = GEOCODING_DIR / settings.files.coordinates

ALIAS_FILE_NAMES = vars(settings.aliases)

# Reference data

@dataclass(frozen=True, slots=True)
class ReferenceData:
    geocoding_overrides: dict[str, dict[str, str]]
    value_mappings: dict[str, str]
    default_values: dict[str, str]
    major_to_academic_field: dict[str, str]

_replacement_data: dict[str, dict[str, str]] = _load_yaml(
    MAPPINGS_DIR / "replacements.yaml"
)

REFERENCE_DATA = ReferenceData(
    geocoding_overrides=_load_yaml(GEOCODING_DIR / "overrides.yaml"),
    value_mappings=_replacement_data["value_mappings"],
    default_values=_replacement_data["default_values"],
    major_to_academic_field=_replacement_data["major_to_academic_field"],
)