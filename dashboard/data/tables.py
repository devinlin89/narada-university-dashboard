import pandas as pd

from config.config import REFERENCE_DATA


def _combine_campuses(campuses: pd.Series) -> str:
    unique_campuses = sorted(
        campus
        for campus in campuses.unique()
        if campus != REFERENCE_DATA.default_values["campus"]
    )

    return ", ".join(unique_campuses) if unique_campuses else "-"


def universities_table(institutions: pd.DataFrame) -> pd.DataFrame:
    """Create the Universities page table."""

    table = (
        institutions
        .groupby(
            ["institution", "country"],
            as_index=False,
        )
        .agg(
            campuses=("campus", _combine_campuses),
            students=("student_count", "sum"),
        )
        .rename(
            columns={
                "institution": "University",
                "campuses": "Campuses",
                "country": "Country",
                "students": "Students",
            }
        )[
            [
                "University",
                "Campuses",
                "Country",
                "Students",
            ]
        ]
        .sort_values(
            "Students",
            ascending=False,
        )
    )

    table.index = range(1, len(table) + 1)
    table.index.name = "#"

    return table


def countries_table(institutions: pd.DataFrame) -> pd.DataFrame:
    """Create the Countries page table."""

    table = (
        institutions
        .groupby("country", as_index=False)
        .agg(
            universities=("institution", "nunique"),
            students=("student_count", "sum"),
        )
        .rename(
            columns={
                "country": "Country",
                "universities": "Universities",
                "students": "Students",
            }
        )[
            [
                "Country",
                "Universities",
                "Students",
            ]
        ]
        .sort_values(
            "Students",
            ascending=False,
        )
    )

    table.index = range(1, len(table) + 1)
    table.index.name = "#"

    return table