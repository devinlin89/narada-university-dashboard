import pandas as pd
import streamlit as st


def entity_selector(
    label: str,
    options: list[str],
) -> str:
    """Display a dropdown for selecting an entity."""

    return st.selectbox(
        label,
        sorted(options),
        index=None,
        placeholder=f"Select a {label.lower()}...",
        width="stretch",
    )

def universities_by_major(
    selected_major: str,
    students_df: pd.DataFrame,
) -> list[str]:
    """Return the unique universities students in the selected major applied to."""

    filtered_students = students_df[
        students_df["major"] == selected_major
    ]

    return filtered_students["institution"].unique().tolist()