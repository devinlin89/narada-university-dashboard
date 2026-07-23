from collections.abc import Callable
from typing import Any

import pandas as pd
from titlecase import titlecase

from aliases.tables import (
    apply_alias_table,
    load_institution_names,
)
from cleaning.campus import clean_campus_name
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
    VALUE_MAPPINGS,
)

# Pipeline Stages

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