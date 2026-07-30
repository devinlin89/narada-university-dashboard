import streamlit as st

from dashboard.data.loader import DashboardData
from dashboard.ui.cards import (
    chart_card,
    info_card,
    metric_card,
)
from dashboard.visualization.charts import (
    academic_field_chart,
    country_bar_chart,
    domestic_pie_chart,
    university_bar_chart,
)
from dashboard.visualization.statistics import DashboardStatistics


def metric_grid(stats: DashboardStatistics) -> None:
    """Display the dashboard summary metrics."""

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card("Students", stats.total_students)

    with col2:
        metric_card("Universities", stats.total_universities)

    with col3:
        metric_card("Countries", stats.total_countries)

    with col4:
        metric_card("Academic Fields", stats.total_fields)


def supporting_charts(data: DashboardData) -> None:
    """Display the supporting dashboard charts."""

    left, right = st.columns(2)

    with left:
        chart_card(
            "Top Countries",
            country_bar_chart(data.institutions),
        )

    with right:
        chart_card(
            "Top Universities",
            university_bar_chart(data.institutions),
        )

    left, right = st.columns(2)

    with left:
        chart_card(
            "Top Academic Fields",
            academic_field_chart(data.students),
        )

    with right:
        chart_card(
            "Domestic vs International",
            domestic_pie_chart(data.students),
        )


def did_you_know(stats: DashboardStatistics) -> None:
    """Display the dashboard insight panel."""

    with st.container(border=True):
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