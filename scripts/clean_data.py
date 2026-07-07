from time import perf_counter

import pandas as pd
from titlecase import titlecase

from config.aliases import ALIAS_FILES
from config.column_names import (
    COLUMN_MAPPING,
    DROPPED_COLUMNS,
    FREE_RESPONSE_COLUMNS,
    LIST_RESPONSE_COLUMNS,
)
from config.logger import (
    configure_logging,
    get_logger,
)
from config.paths import (
    PROCESSED_DATA,
    RAW_DATA,
)
from config.replacements import (
    DEFAULT_VALUES,
    VALUE_MAPPINGS,
    MAJOR_TO_ACADEMIC_FIELD,
)
from utils.alias import (
    load_institution_names,
    apply_alias_table,
)
from utils.campus import clean_campus_name

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
    # Apply default values

    for column, default in DEFAULT_VALUES.items():
        df[column] = (
            df[column]
            .fillna(default)
            .replace({"-": default})
        )

    return df


def clean_free_response(value: object) -> object:
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


def apply_aliases(df: pd.DataFrame) -> pd.DataFrame:
    # Apply alias mappings to configured columns

    for column in ALIAS_FILES:
        df[column] = apply_alias_table(df[column], column)

    return df


def export_data(df: pd.DataFrame) -> None:
    # Save the cleaned dataset CSV file

    PROCESSED_DATA.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_DATA, index=False)


# Main Function

def main() -> None:
    configure_logging()

    start_time = perf_counter()

    try:
        logger.info("Loading raw dataset...")
        df = load_data()

        logger.info("Loaded %d rows.", len(df))

        logger.info("Applying schema...")
        df = apply_schema(df)

        logger.info("Normalizing values...")
        df = normalize_values(df)

        logger.info("Converting list fields...")
        df = normalize_lists(df)

        logger.info("Applying default values...")
        df = apply_defaults(df)

        logger.info("Normalizing text...")
        df = normalize_text(df)

        logger.info("Normalizing campus names...")
        df = normalize_campuses(df)

        logger.info("Applying aliases...")
        df = apply_aliases(df)

        logger.info("Exporting cleaned dataset...")
        export_data(df)

        logger.info("Exported cleaned dataset to %s", PROCESSED_DATA)
        logger.info("Data cleaning completed successfully.")

    except Exception:
        logger.exception("Data cleaning failed.")
        raise

    finally:
        elapsed = perf_counter() - start_time
        logger.info("Total execution time: %.3f s.", elapsed)


if __name__ == "__main__":
    main()