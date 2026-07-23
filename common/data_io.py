from pathlib import Path

import pandas as pd

from config.config import (
    COORDINATES_DATA,
    INSTITUTIONS_DATA,
    RAW_DATA,
    STUDENTS_DATA,
)


def load_raw_data() -> pd.DataFrame:
    # Load the raw Google Forms export into a DataFrame
    return pd.read_csv(RAW_DATA)


def load_csv_or_empty(path: Path, columns: list[str]) -> pd.DataFrame:
    # Load a CSV file or return an empty DataFrame if it does not exist

    if not path.exists():
        return pd.DataFrame(columns=columns)

    return pd.read_csv(path)


def load_students() -> pd.DataFrame:
    # Load the processed student dataset

    return pd.read_csv(STUDENTS_DATA)


def load_institutions() -> pd.DataFrame:
    # Load the processed institution dataset

    return pd.read_csv(INSTITUTIONS_DATA)


def load_coordinates() -> pd.DataFrame:
    # Load the processed coordinates dataset

    # If the coordinates file does not exist,
    # return an empty DataFrame with the expected columns
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