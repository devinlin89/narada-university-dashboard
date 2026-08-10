import streamlit as st

from dashboard.data.loader import DashboardData
from dashboard.data.statistics import DashboardStatistics
from dashboard.ui.cards import (
    chart_card,
    info_card,
)
from dashboard.ui.layout import (
    metric_row,
    navigation_grid,
)
from dashboard.visualization.flags import country_flag
from dashboard.visualization.overview import (
    overview_academic_field_chart,
    overview_country_bar_chart,
    overview_domestic_donut_chart,
    overview_jabodetabek_donut_chart,
    overview_program_type_chart,
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
            "Program Types",
            overview_program_type_chart(data.students),
        )

    left, right = st.columns(2)

    with left:
        chart_card(
            "Domestic vs International",
            overview_domestic_donut_chart(data.students),
        )

    with right:
        chart_card(
            "Indonesian Destinations",
            overview_jabodetabek_donut_chart(data.students),
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
                (
                        f"{country_flag(stats.most_popular_country)} "
                        f"{stats.most_popular_country}"
                ),
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

        navigation_grid()