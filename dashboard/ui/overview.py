import streamlit as st

from dashboard.data.loader import DashboardData
from dashboard.data.statistics import DashboardStatistics
from dashboard.ui.cards import (
    chart_card,
    info_card,
    navigation_card,
)
from dashboard.ui.layout import metric_row
from dashboard.visualization.overview import (
    overview_academic_field_chart,
    overview_country_bar_chart,
    overview_domestic_pie_chart,
    overview_university_bar_chart,
)


def metric_grid(stats: DashboardStatistics) -> None:
    """Display the dashboard summary metrics."""

    metric_row(
        ("Students", stats.total_students),
        ("Universities", stats.total_universities),
        ("Countries", stats.total_countries),
        ("Academic Fields", stats.total_fields),
    )


def supporting_charts(data: DashboardData) -> None:
    """Display the supporting dashboard charts."""

    left, right = st.columns(2)

    with left:
        chart_card(
            "Top Countries",
            overview_country_bar_chart(data.institutions),
        )

    with right:
        chart_card(
            "Top Universities",
            overview_university_bar_chart(data.institutions),
        )

    left, right = st.columns(2)

    with left:
        chart_card(
            "Top Academic Fields",
            overview_academic_field_chart(data.students),
        )

    with right:
        chart_card(
            "Domestic vs International",
            overview_domestic_pie_chart(data.students),
        )


def did_you_know(stats: DashboardStatistics) -> None:
    """Display the dashboard insight panel."""

    with st.container():
        st.subheader("💡 Did You Know?")

        top_left, top_right = st.columns(2)

        with top_left:
            info_card(
                "🏛️",
                "Most Popular University",
                stats.most_popular_university,
            )

        with top_right:
            info_card(
                "🌍",
                "Most Popular Country",
                stats.most_popular_country,
            )

        bottom_left, bottom_right = st.columns(2)

        with bottom_left:
            info_card(
                "🎓",
                "Most Popular Academic Field",
                stats.most_popular_field,
            )

        with bottom_right:
            info_card(
                "✈️",
                "Farthest Destination",
                stats.farthest_destination,
            )


def explore_more() -> None:
    """Display the explore more section"""

    with st.container(border=True):
        st.subheader("🔎 Explore More")

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