from collections.abc import Callable
from time import perf_counter
from typing import Any

import pandas as pd
from titlecase import titlecase

from config.column_names import (
    COLUMN_MAPPING,
    DROPPED_COLUMNS,
    FREE_RESPONSE_COLUMNS,
    LIST_RESPONSE_COLUMNS,
)
from config.config import (
    ALIAS_FILES,
    DEFAULT_VALUES,
    MAJOR_TO_ACADEMIC_FIELD,
    PROCESSED_DATA_DIR,
    RAW_DATA,
    STUDENTS_DATA,
    VALUE_MAPPINGS,
)
from config.logger import (
    configure_logging,
    get_logger,
)
from utils.alias import (
    apply_alias_table,
    load_institution_names,
)
from utils.campus import clean_campus_name
from utils.validation import (
    validate_aliases,
    validate_boolean_columns,
    validate_list_columns,
    validate_required_fields,
)

logger = get_logger("scripts.clean_data")

# Pipeline Stages

def load_data() -> pd.DataFrame:
    # Load the raw Google Forms export into a DataFrame
    return pd.read_csv(RAW_DATA)


def apply_schema(df: pd.DataFrame) -> pd.DataFrame:
    # Rename columns and remove unused columns

    df = df.rename(columns=COLUMN_MAPPING)
    df = df.drop(columns=DROPPED_COLUMNS)

    return df


def normalize_values(df: pd.DataFrame) -> pd.DataFrame:
    # Apply configured value mappings

    for column, mapping in VALUE_MAPPINGS.items():
        df[column] = df[column].replace(mapping)

    return df


def normalize_lists(df: pd.DataFrame) -> pd.DataFrame:
    # Convert comma-separated response strings into Python lists

    for column in LIST_RESPONSE_COLUMNS:
        df[column] = df[column].str.split(", ")

    return df


def apply_defaults(df: pd.DataFrame) -> pd.DataFrame:
    # Apply configured default values

    for column, default in DEFAULT_VALUES.items():
        df[column] = (
            df[column]
            .fillna(default)
            .replace({"-": default})
        )

    return df


def clean_free_response(value: Any) -> Any:
    # Normalize a free-response string by trimming whitespace and applying title case

    if not isinstance(value, str):
        return value

    return titlecase(value.strip())


def normalize_text(df: pd.DataFrame) -> pd.DataFrame:
    # Standardize free-response text

    for column in FREE_RESPONSE_COLUMNS:
        df[column] = df[column].apply(clean_free_response)

    return df


def normalize_campuses(df: pd.DataFrame) -> pd.DataFrame:
    # Remove institution names and countries from campus names

    institution_names = load_institution_names()

    df["campus"] = df["campus"].apply(
        lambda campus: clean_campus_name(campus, institution_names)
    )

    return df


def normalize_academic_fields(df: pd.DataFrame) -> pd.DataFrame:
    # Correct academic fields for known majors

    field = df["major"].map(MAJOR_TO_ACADEMIC_FIELD)

    df["academic_field"] = field.fillna(df["academic_field"])

    return df


def infer_single_campuses(df: pd.DataFrame) -> pd.DataFrame:
    # Replace "Not Specified" with the only known campus.

    # Find all known campuses for each institution
    known_campuses = (
        df.loc[df["campus"] != "Not Specified"]
        .groupby("institution")["campus"]
        .unique()
    )

    # Build a mapping for institutions with only one known campus
    replacements = {
        institution: campuses[0]
        for institution, campuses in known_campuses.items()
        if len(campuses) == 1
    }

    # Select rows where the campus is "Not Specified"
    # and the institution has a single known campus
    mask = (
        df["campus"].eq("Not Specified")
        & df["institution"].isin(replacements)
    )

    # Replace "Not Specified" with the inferred campus name
    df.loc[mask, "campus"] = (
        df.loc[mask, "institution"]
        .map(replacements)
    )

    return df


def apply_aliases(df: pd.DataFrame) -> pd.DataFrame:
    # Apply alias mappings to configured columns

    for column in ALIAS_FILES:
        df[column] = apply_alias_table(df[column], column)

    return df


def sort_dataset(df: pd.DataFrame) -> pd.DataFrame:
    # Sort the cleaned dataset

    columns_sorting_order = [
        "country",
        "institution",
        "campus",
        "major",
    ]

    return (
        df.sort_values(columns_sorting_order)
        .reset_index(drop=True)
    )

def validate_dataset(df: pd.DataFrame) -> None:
    # Validate the cleaned dataset before export

    validate_required_fields(df)
    validate_boolean_columns(df)
    validate_list_columns(df)
    validate_aliases(df)


def export_data(df: pd.DataFrame) -> None:
    # Save the cleaned dataset CSV file

    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(STUDENTS_DATA, index=False)


# Pipeline Definition

StageFunction = Callable[[pd.DataFrame], pd.DataFrame]
PipelineStage = tuple[str, StageFunction]

PIPELINE: tuple[PipelineStage, ...] = (
    # (Log message, stage function)
    ("Applying schema...", apply_schema),
    ("Normalizing values...", normalize_values),
    ("Converting list fields...", normalize_lists),
    ("Applying default values...", apply_defaults),
    ("Normalizing text...", normalize_text),
    ("Normalizing campus names...", normalize_campuses),
    ("Normalizing academic fields...", normalize_academic_fields),
    ("Inferring single campuses...", infer_single_campuses),
    ("Applying aliases...", apply_aliases),
    ("Sorting dataset...", sort_dataset),
)


def run_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    # Run the data cleaning pipeline

    for message, stage in PIPELINE:
        logger.info(message)
        df = stage(df)

    return df


# Main Function

def main() -> None:
    configure_logging()

    start_time = perf_counter()

    try:
        logger.info("Loading raw dataset...")
        df = load_data()

        logger.info("Loaded %d rows.", len(df))

        df = run_pipeline(df)

        logger.info("Validating dataset...")
        validate_dataset(df)

        logger.info("Exporting cleaned dataset...")
        export_data(df)

        logger.info("Exported cleaned dataset to %s", STUDENTS_DATA)

        logger.info(
            "Dataset summary: %d students, %d institutions, %d majors.",
            len(df),
            df["institution"].nunique(),
            df["major"].nunique(),
        )

        logger.info("Data cleaning completed successfully.")

    except Exception:
        logger.exception("Data cleaning failed.")
        raise

    finally:
        elapsed = perf_counter() - start_time
        logger.info("Total execution time: %.3f s.", elapsed)


if __name__ == "__main__":
    main()