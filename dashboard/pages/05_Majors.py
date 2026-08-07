import streamlit as st

from dashboard.ui.filters import entity_selector
from dashboard.data.loader import load_dashboard_data
from dashboard.data.tables import majors_table
from dashboard.ui.cards import (
    page_header,
    primary_section,
)
from dashboard.ui.styles import load_css
from dashboard.visualization.majors import academic_field_distribution_chart

data = load_dashboard_data()

load_css()

page_header(
    title="Majors",
    description=(
        "Explore the majors and academic fields chosen by students "
        "and discover where those programs are offered around the world."
    ),
)

with primary_section(
    title="Academic Field Distribution",
    description=(
        "Compare the academic fields chosen by the graduating class. "
        "Each field groups together related majors to provide a higher-level "
        "view of students' areas of study."
    ),
):
    st.plotly_chart(
        academic_field_distribution_chart(data.students),
        width="stretch",
        config={"displayModeBar": False},
    )

st.subheader("University Selector")

selected_major = entity_selector(
    "Major",
    data.students["major"].unique(),
)

if selected_major is None:
    st.info("Select a major to see the universities students in that major applied to.")


st.dataframe(
    majors_table(data.students),
    width="stretch",
)
