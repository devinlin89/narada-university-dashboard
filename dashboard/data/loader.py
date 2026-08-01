from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import streamlit as st

from config.config import (
    COORDINATES_DATA,
    INSTITUTIONS_DATA,
    STUDENTS_DATA,
)
from dashboard.data.statistics import DashboardStatistics


@dataclass(frozen=True)
class DashboardData:
    students: pd.DataFrame
    institutions: pd.DataFrame
    statistics: DashboardStatistics

@st.cache_data
def load_csv(file_path: Path) -> pd.DataFrame:
    """Load a CSV file with Streamlit caching."""

    return pd.read_csv(file_path)


@st.cache_data
def load_dashboard_data() -> DashboardData:
    """Load and prepare all dashboard datasets."""

    students = load_csv(STUDENTS_DATA)

    institutions = load_csv(INSTITUTIONS_DATA)

    coordinates = load_csv(COORDINATES_DATA)

    institutions = institutions.merge(
        coordinates,
        on=["institution", "campus", "country"],
        how="left",
        validate="one_to_one",
    )

    return DashboardData(
        students=students,
        institutions=institutions,
        statistics=DashboardStatistics.from_data(
        students,
        institutions,
    ),
    )