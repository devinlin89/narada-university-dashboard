import streamlit as st

from dashboard.data.loader import load_dashboard_data
from dashboard.data.profile import scholarship_statistics
from dashboard.data.tables import admissions_table
from dashboard.ui.cards import page_header, primary_section, vertical_spacer
from dashboard.ui.layout import metric_row
from dashboard.ui.styles import load_css
from dashboard.visualization.admissions import (
    applications_distribution_chart,
    decision_factors_chart,
    offers_distribution_chart,
    scholarship_benefits_chart,
)

data = load_dashboard_data()

load_css()

page_header(
    title="Admissions",
    description=(
        "Explore how many universities students applied to, the offers they "
        "received, and their scholarship outcomes to understand the admissions "
        "outcomes of the Class of 2026."
    ),
)


metric_row(
    ("Total Respondents", data.statistics.total_students),
    ("Average Applications", f"{data.statistics.average_applications:.1f}"),
    ("Average Offer Rate", f"{data.statistics.average_offer_rate:.0%}"),
    ("Scholarship Recipients", data.statistics.received_scholarship),
)


with primary_section(
    title="University Applications",
    description=(
        "Explore how many universities students applied to during this "
        "admissions cycle. This provides an overview of application "
        "strategies across the graduating class."
    ),
):
    st.plotly_chart(
        applications_distribution_chart(data.students),
        width="stretch",
        config={"displayModeBar": False},
    )


with primary_section(
    title="University Offers",
    description=(
        "Explore how many university offers students received this "
        "admissions cycle. This provides an overview of admission "
        "outcomes across the graduating class."
    ),
):
    st.plotly_chart(
        offers_distribution_chart(data.students),
        width="stretch",
        config={"displayModeBar": False},
    )


with primary_section(
    title="Decision Factors",
    description=(
        "Explore the factors students considered when making their "
        "university decisions. Students could select multiple factors."
    ),
):
    st.plotly_chart(
        decision_factors_chart(data.students),
        width="stretch",
        config={"displayModeBar": False},
    )


with primary_section(
    title="Scholarships",
    description=(
        "Explore scholarships received and the types of financial "
        "support received by students."
    ),
):
    scholarship_stats = scholarship_statistics(data.students)

    vertical_spacer()

    left, middle, right = st.columns(3)

    with left:
        st.metric(
            "Received Scholarship",
            scholarship_stats.received,
        )

    with middle:
        st.metric(
            "No Response",
            scholarship_stats.no_response,
        )

    with right:
        st.metric(
            "No Scholarship",
            scholarship_stats.no_scholarship,
        )

    st.markdown("#### Scholarship Types")

    st.plotly_chart(
        scholarship_benefits_chart(data.students),
        width="stretch",
        config={"displayModeBar": False},
    )


st.subheader("Admissions Table")

st.dataframe(
    admissions_table(data.students),
    width="stretch",
)