import pandas as pd
import streamlit as st

from dashboard.data.profile import university_profile
from dashboard.ui.cards import (
    chart_card,
    university_result_card,
)
from dashboard.ui.layout import metric_row
from dashboard.visualization.majors import major_country_distribution_chart


def display_major_results(
    academic_field: str | None,
    major: str | None,
    students_df: pd.DataFrame,
) -> None:
    """Display destination results for the selected academic field or major."""

    if major:
        filtered_students = students_df.loc[
            students_df["major"].eq(major)
        ]
    elif academic_field:
        filtered_students = students_df.loc[
            students_df["academic_field"].eq(academic_field)
        ]
    else:
        st.info(
            "Select an academic field or major to explore university "
            "destinations."
        )
        return

    metric_row(
        ("Total Students", len(filtered_students)),
        ("Universities", filtered_students["institution"].nunique()),
        ("Countries / Regions", filtered_students["country"].nunique()),
        (
            "International Rate",
            f"{filtered_students['country'].ne('Indonesia').mean():.0%}",
        ),
    )

    chart_card(
        "Country / Region Distribution",
        major_country_distribution_chart(filtered_students),
    )


def display_university_results(
    academic_field: str | None,
    major: str | None,
    students_df: pd.DataFrame,
    institutions_df: pd.DataFrame,
) -> None:
    """Display universities matching the selected academic field or major."""

    if major:
        filter_column = "major"
        filter_value = major
    elif academic_field:
        filter_column = "academic_field"
        filter_value = academic_field
    else:
        return

    filtered_students = students_df.loc[
        students_df[filter_column].eq(filter_value)
    ]

    university_profiles = sorted(
        (
            university_profile(
                university,
                institutions_df,
                student_count=int(
                    filtered_students["institution"]
                    .eq(university)
                    .sum()
                ),
            )
            for university in filtered_students["institution"].unique()
        ),
        key=lambda profile: profile.students,
        reverse=True,
    )

    for i in range(0, len(university_profiles), 2):
        cols = st.columns(2)

        for j, profile in enumerate(university_profiles[i:i + 2]):
            with cols[j]:
                university_result_card(
                    profile,
                    filter_column,
                    "profile-content--short",
                )