# utils/data_io.py

import pandas as pd

from config.paths import (
    STUDENTS_DATA,
)


def load_students() -> pd.DataFrame:
    # Load the processed student dataset

    return pd.read_csv(STUDENTS_DATA)