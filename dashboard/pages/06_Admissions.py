import streamlit as st

from dashboard.data.loader import load_dashboard_data
from dashboard.data.tables import admissions_table
from dashboard.ui.cards import (
    page_header,
    primary_section,
)
from dashboard.ui.styles import load_css
from dashboard.visualization.admissions import applications_distribution_chart

data = load_dashboard_data()

load_css()

page_header(
    title="Admissions",
    description=(
        "Explore how many universities students applied to, the offers they "
        "received, and their scholarship outcomes understand the "
        "admissions outcomes of the Class of 2026."
    ),
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

st.dataframe(
    admissions_table(data.students),
    width="stretch",
)
