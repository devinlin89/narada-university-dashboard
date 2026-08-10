from collections.abc import Callable

import streamlit as st

from dashboard.ui.cards import (
    metric_card,
    navigation_card,
)


def two_column_layout(
    left_content: Callable[[], None],
    right_content: Callable[[], None],
) -> None:
    """Display two pieces of content side by side."""

    left, right = st.columns(2)

    with left:
        left_content()

    with right:
        right_content()


def metric_row(
    *metrics: tuple[str, str | int | float],
) -> None:
    """Display metrics in a single row."""

    columns = st.columns(len(metrics))

    for column, (label, value) in zip(columns, metrics):
        with column:
            metric_card(label, value)


def navigation_grid():
    top_left, top_right = st.columns(2)

    with top_left:
        navigation_card(
                title="World Map",
                icon="🗺️",
                description=(
                "Explore every university destination "
                "on an interactive world map."
                ),
                page="pages/02_World_Map.py",
            )

    with top_right:
        navigation_card(
                title="Universities",
                icon="🏛️",
                description=(
                "Browse all universities, student counts, " 
                "and destination campuses."
                ),
                page="pages/03_Universities.py",
            )

    middle_left, middle_right = st.columns(2)


    with middle_left:
        navigation_card(
                title="Countries",
                icon="🌍",
                description=(
                "See destination countries and "
                "how students are distributed worldwide."
                ),
                page="pages/04_Countries.py",
            )

    with middle_right:
        navigation_card(
                title="Majors",
                icon="🎓",
                description=(
                "Explore the most popular majors and "
                "academic fields chosen by students."
                ),
                page="pages/05_Majors.py",
            )


    bottom_left, bottom_right = st.columns(2)


    with bottom_left:
        navigation_card(
                title="Admissions",
                icon="📝",
                description=(
                "Analyze application count, admission offers, "
                "and scholarship outcomes."
                ),
                page="pages/06_Admissions.py",
            )

    with bottom_right:
        navigation_card(
                title="About",
                icon="ℹ️",
                description=(
                "Learn how this dashboard was built and "
                "where the data comes from."
                ),
                page="pages/07_About.py",
            )