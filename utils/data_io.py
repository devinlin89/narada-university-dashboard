# utils/data_io.py

import pandas as pd

from config.paths import (
    COORDINATES_DATA,
    INSTITUTIONS_DATA,
    STUDENTS_DATA,
)


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