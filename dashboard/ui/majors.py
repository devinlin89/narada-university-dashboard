import pandas as pd
import streamlit as st

from dashboard.data.profile import university_profile
from dashboard.ui.cards import university_profile_card
from dashboard.ui.layout import metric_row


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
        st.info(
            "Select an academic field or major to see the universities "
            "students applied to."
        )
        return

    filtered_students = students_df.loc[
        students_df[filter_column].eq(filter_value)
    ]

    metric_row(
        ("Total Students", len(filtered_students)),
        (
            "Most Common Country",
            filtered_students["country"].mode().iat[0],
        ),
    )

    university_profiles = [
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
    ]

    for i in range(0, len(university_profiles), 2):
        cols = st.columns(2)

        for j, profile in enumerate(university_profiles[i:i + 2]):
            with cols[j]:
                university_profile_card(
                    profile,
                    "profile-content--short"
                )