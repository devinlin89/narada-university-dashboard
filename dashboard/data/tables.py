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
                "country": "Country / Region",
                "students": "Students",
            }
        )[
            [
                "University",
                "Campuses",
                "Country / Region",
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
    """Create the Countries/Regions page table."""

    table = (
        institutions
        .groupby("country", as_index=False)
        .agg(
            universities=("institution", "nunique"),
            students=("student_count", "sum"),
        )
        .rename(
            columns={
                "country": "Country / Region",
                "universities": "Universities",
                "students": "Students",
            }
        )[
            [
                "Country / Region",
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


def majors_table(students: pd.DataFrame) -> pd.DataFrame:
    """Create the Majors page table."""

    table = (
        students
        .groupby(
            ["academic_field", "major"],
            as_index=False,
        )
        .size()
        .rename(
            columns={
                "academic_field": "Academic Field",
                "major": "Major",
                "size": "Students",
            }
        )[
            [
                "Academic Field",
                "Major",
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


def admissions_table(students: pd.DataFrame) -> pd.DataFrame:
    """Create the Admissions page table."""

    table = (
        students
        .rename(
            columns={
                "applications_count": "Applications",
                "acceptances_count": "Offers",
                "received_scholarship?": "Scholarship",
                "scholarship_description": "Scholarship Description",
                "decision_factors": "Decision Factors",
            }
        )
        .assign(
            **{
                "Offer Rate": lambda df: (
                    df["Offers"] / df["Applications"]
                ).map("{:.0%}".format),
                "Decision Factors": lambda df: (
                    df["Decision Factors"]
                    .apply(", ".join)
                ),
            }
        )[
            [
                "Applications",
                "Offers",
                "Offer Rate",
                "Scholarship",
                "Scholarship Description",
                "Decision Factors",
            ]
        ]
        .sort_values(
            "Offers",
            ascending=False,
        )
    )

    table.index = range(1, len(table) + 1)
    table.index.name = "#"

    return table