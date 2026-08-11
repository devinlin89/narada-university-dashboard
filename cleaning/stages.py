from collections.abc import Callable
from dataclasses import dataclass
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
    ALIAS_FILE_NAMES,
    REFERENCE_DATA,
)

# Cleaning pipeline stages


def apply_schema(df: pd.DataFrame) -> pd.DataFrame:
    """Rename columns, drop unused fields, and normalize invisible characters.

    Args:
        df (pd.DataFrame): Input DataFrame with raw column names to normalize.

    Returns:
        pd.DataFrame: DataFrame with columns renamed using COLUMN_MAPPING and
            unused columns removed.
    """

    df.columns = df.columns.str.replace("\r\n", "\n")

    df = df.rename(columns=COLUMN_MAPPING)
    df = df.drop(columns=DROPPED_COLUMNS)

    return df


def normalize_values(df: pd.DataFrame) -> pd.DataFrame:
    """Replace column values using configured reference mappings.

    Args:
        df (pd.DataFrame): DataFrame containing columns with values to normalize.

    Returns:
        pd.DataFrame: DataFrame with values mapped according to
            REFERENCE_DATA.value_mappings.
    """

    for column, mapping in REFERENCE_DATA.value_mappings.items():
        df[column] = df[column].replace(mapping)

    return df


def normalize_lists(df: pd.DataFrame) -> pd.DataFrame:
    """Convert comma-separated response strings into Python lists.

    Args:
        df (pd.DataFrame): DataFrame containing list response columns.

    Returns:
        pd.DataFrame: DataFrame with each LIST_RESPONSE_COLUMNS field converted to
            a list of response strings.
    """

    for column in LIST_RESPONSE_COLUMNS:
        df[column] = df[column].str.split(", ")

    return df


def apply_defaults(df: pd.DataFrame) -> pd.DataFrame:
    """Fill missing values and placeholder entries with configured defaults.

    Args:
        df (pd.DataFrame): DataFrame to apply default values to.

    Returns:
        pd.DataFrame: DataFrame with missing values filled and placeholder
            "-" entries replaced by defaults from REFERENCE_DATA.default_values.
    """

    for column, default in REFERENCE_DATA.default_values.items():
        df[column] = df[column].fillna(default).replace({"-": default})

    return df


def clean_free_response(value: Any) -> Any:
    """Normalize a free-response value by trimming whitespace and title-casing text.

    Args:
        value (Any): Value from a free-response column.

    Returns:
        Any: Normalized string if the input is a str, otherwise the original value.
    """

    if not isinstance(value, str):
        return value

    return titlecase(value.strip())


def normalize_text(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize free-response text.

    Args:
        df (pd.DataFrame): DataFrame containing free-response columns.

    Returns:
        pd.DataFrame: DataFrame with free-response columns normalized.
    """

    for column in FREE_RESPONSE_COLUMNS:
        df[column] = df[column].apply(clean_free_response)

    return df


def normalize_campuses(df: pd.DataFrame) -> pd.DataFrame:
    """Remove institution names and countries/regions from campus names.

    Args:
        df (pd.DataFrame): DataFrame containing the "campus" column.

    Returns:
        pd.DataFrame: DataFrame with normalized campus names.
    """

    institution_names = load_institution_names()

    df["campus"] = df["campus"].apply(
        lambda campus: clean_campus_name(campus, institution_names)
    )

    return df


def normalize_academic_fields(df: pd.DataFrame) -> pd.DataFrame:
    """Update academic field values based on known major-to-field mappings.

    This stage uses the configured major-to-academic-field mapping in
    REFERENCE_DATA to replace academic field values when a major has a known
    corresponding academic field. Existing academic field values are preserved
    when no mapping is found.

    Args:
        df (pd.DataFrame): DataFrame containing at the
            "major" and "academic_field" columns.

    Returns:
        pd.DataFrame: DataFrame with academic field values updated for mapped
            majors while leaving unmapped values unchanged.
    """

    field = df["major"].map(REFERENCE_DATA.major_to_academic_field)

    df["academic_field"] = field.fillna(df["academic_field"])

    return df


def infer_single_campuses(df: pd.DataFrame) -> pd.DataFrame:
    """Infer and fill missing campus values when an institution has one campus.

    For institutions where only a single non-default campus value appears in
    the dataset, replace any rows that currently have the configured default
    campus value with that single known campus. This helps populate missing
    campus information when it is unambiguous.

    Args:
        df (pd.DataFrame): Students dataset containing the
            "institution" and "campus" columns.

    Returns:
        pd.DataFrame: DataFrame with inferred campus values applied
            where appropriate.
    """

    # Collect all non-default campuses for each institution
    known_campuses = (
        df.loc[df["campus"] != REFERENCE_DATA.default_values["campus"]]
        .groupby("institution")["campus"]
        .unique()
    )

    # Build a mapping for institutions with only one known campus
    replacements = {
        institution: campuses[0]
        for institution, campuses in known_campuses.items()
        if len(campuses) == 1
    }

    # Select rows with the default campus value
    # whose institution has exactly one known campus
    mask = df["campus"].eq(REFERENCE_DATA.default_values["campus"]) & df[
        "institution"
    ].isin(replacements)

    # Replace campus default value with the inferred campus name
    df.loc[mask, "campus"] = df.loc[mask, "institution"].map(replacements)

    return df


def apply_aliases(df: pd.DataFrame) -> pd.DataFrame:
    """Apply alias mappings to configured columns.

    The alias tables defined in ALIAS_FILE_NAMES are loaded and applied to
    each corresponding column in the provided DataFrame. This standardizes
    values using the alias reference data.

    Args:
        df (pd.DataFrame): DataFrame containing columns to normalize with
            alias mappings.

    Returns:
        pd.DataFrame: DataFrame with alias mappings applied for
            configured columns.
    """

    for column in ALIAS_FILE_NAMES:
        df[column] = apply_alias_table(df[column], column)

    return df


def sort_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Sort the cleaned students dataset.

    Args:
        df (pd.DataFrame): DataFrame containing processed student data to sort

    Returns:
        pd.DataFrame: Sorted DataFrame by country, institution, campus, and major
    """

    columns_sorting_order = [
        "country",
        "institution",
        "campus",
        "major",
    ]

    return df.sort_values(columns_sorting_order).reset_index(drop=True)


# Cleaning pipeline definition

type StageFunction = Callable[[pd.DataFrame], pd.DataFrame]


@dataclass(frozen=True)
class CleaningStage:
    """A single stage in a data processing pipeline.

    Args:
        message (str): Message displayed while the stage runs.
        function (StageFunction): Function executed by the stage.
    """

    message: str
    function: StageFunction


CLEANING_STAGES: tuple[CleaningStage, ...] = (
    # (Log message, stage function)
    CleaningStage("Applying schema...", apply_schema),
    CleaningStage("Normalizing values...", normalize_values),
    CleaningStage("Converting list fields...", normalize_lists),
    CleaningStage("Applying default values...", apply_defaults),
    CleaningStage("Normalizing text...", normalize_text),
    CleaningStage("Normalizing campus names...", normalize_campuses),
    CleaningStage("Normalizing academic fields...", normalize_academic_fields),
    CleaningStage("Inferring single campuses...", infer_single_campuses),
    CleaningStage("Applying aliases...", apply_aliases),
    CleaningStage("Sorting dataset...", sort_dataset),
)
