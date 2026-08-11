import pandas as pd

from aliases.tables import load_alias_table
from common.exceptions import ValidationError
from config.column_names import (
    BOOLEAN_COLUMNS,
    LIST_RESPONSE_COLUMNS,
    REQUIRED_COLUMNS,
)
from config.config import ALIAS_FILE_NAMES


def csv_rows(mask: pd.Series) -> list[int]:
    """Convert a boolean mask to 1-based CSV row numbers.

    Args:
        mask (pd.Series): Boolean Series identifying rows of interest.

    Returns:
        list[int]: CSV row numbers corresponding to the true values in the mask.
    """

    return (mask[mask].index + 2).tolist()


def validate_required_fields(df: pd.DataFrame) -> None:
    """Validate that all required fields contain non-empty values.

    Args:
        df (pd.DataFrame): DataFrame to validate.

    Raises:
        ValidationError: If any required field contains a missing or empty value.
    """

    for column in REQUIRED_COLUMNS:
        missing = df[column].isna() | (df[column].astype(str).str.strip().eq(""))

        if missing.any():
            rows = csv_rows(missing)

            raise ValidationError(
                f"Required field '{column}' contains missing values on CSV rows: {rows}"
            )


def validate_column_type(
    df: pd.DataFrame,
    columns: tuple[str, ...] | list[str],
    expected_type: type,
) -> None:
    """Validate the types of non-null values in specified columns.

    Args:
        df (pd.DataFrame): DataFrame to validate.
        columns (tuple[str, ...] | list[str]): Columns whose values should
            be validated.
        expected_type (type): Expected Python type for the column values.

    Raises:
        ValidationError: If any non-null value does not have the expected type.
    """

    for column in columns:
        invalid = (
            df[column]
            .dropna()
            .apply(lambda value: not isinstance(value, expected_type))
        )

        if invalid.any():
            rows = csv_rows(invalid)

            raise ValidationError(
                f"Column '{column}' contains invalid "
                f"{expected_type.__name__} values on CSV rows: {rows}"
            )


def validate_boolean_columns(df: pd.DataFrame) -> None:
    """Validate that boolean columns contain only boolean values.

    Args:
        df (pd.DataFrame): DataFrame to validate.

    Raises:
        ValidationError: If any non-null value in a boolean column is not 
            a boolean.
    """

    validate_column_type(
        df,
        BOOLEAN_COLUMNS,
        bool,
    )


def validate_list_columns(df: pd.DataFrame) -> None:
    """Validate that list-response columns contain only lists.

    Args:
        df (pd.DataFrame): DataFrame to validate.

    Raises:
        ValidationError: If any non-null value in a list-response column is
            not a list.
    """

    validate_column_type(
        df,
        LIST_RESPONSE_COLUMNS,
        list,
    )


def validate_aliases(df: pd.DataFrame) -> None:
    """Validate that no unresolved aliases remain in the dataset.

    Args:
        df (pd.DataFrame): Cleaned DataFrame to validate.

    Raises:
        ValidationError: If any unresolved alias remains in an alias-managed
            column.
    """

    for column in ALIAS_FILE_NAMES:
        alias_df = load_alias_table(column)

        unresolved_aliases = set(
            alias_df.loc[
                alias_df["alias"] != alias_df["canonical"],
                "alias",
            ]
            .dropna()
            .astype(str)
        )

        remaining = sorted(set(df[column].dropna().astype(str)) & unresolved_aliases)

        if remaining:
            raise ValidationError(
                f"Column '{column}' still contains unresolved aliases: "
                f"{', '.join(remaining)}"
            )