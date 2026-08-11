from pathlib import Path

import pandas as pd

from config.config import (
    COORDINATES_DATA,
    INSTITUTIONS_DATA,
    RAW_DATA,
    STUDENTS_DATA,
)


def load_raw_data() -> pd.DataFrame:
    """Load the raw Google Forms export into a DataFrame.

    Returns:
        pd.DataFrame: DataFrame containing the raw Google Forms data.
    """

    return pd.read_csv(RAW_DATA)


def load_csv_or_empty(path: Path, columns: list[str]) -> pd.DataFrame:
    """Load a CSV file or return an empty DataFrame if it is missing or empty.

    Args:
        path (Path): Path to the CSV file.
        columns (list[str]): Column names for the empty DataFrame.

    Returns:
        pd.DataFrame: DataFrame containing the CSV data, or an empty
            DataFrame with the specified columns if the file is missing
            or empty.
    """

    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame(columns=columns)

    return pd.read_csv(path)


def load_students() -> pd.DataFrame:
    """Load the processed student dataset.

    Returns:
        pd.DataFrame: DataFrame containing the processed student data.
    """

    return pd.read_csv(STUDENTS_DATA)


def load_institutions() -> pd.DataFrame:
    """Load the processed institution dataset.

    Returns:
        pd.DataFrame: DataFrame containing institution, campus, country,
            and student count data.
    """

    return pd.read_csv(INSTITUTIONS_DATA)


def load_coordinates() -> pd.DataFrame:
    """Load the processed coordinates dataset.

    Returns:
        pd.DataFrame: DataFrame containing processed coordinates data,
            or an empty DataFrame with the expected columns
            if the dataset does not exist.
    """

    # Return an empty DataFrame with the expected columns if the file is missing.
    if not COORDINATES_DATA.exists():
        return pd.DataFrame(
            columns=[
                "institution",
                "campus",
                "country",
                "latitude",
                "longitude",
            ]
        )

    return pd.read_csv(COORDINATES_DATA)