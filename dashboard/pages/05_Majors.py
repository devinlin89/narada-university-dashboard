import streamlit as st

from dashboard.data.loader import load_dashboard_data
from dashboard.data.tables import majors_table
from dashboard.ui.cards import (
    page_header,
    primary_section,
)
from dashboard.ui.filters import entity_selector
from dashboard.ui.majors import display_university_results
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

st.subheader("Academic Field and Major Selector")

left, right = st.columns(2)

with left:
    selected_academic_field = entity_selector(
        "Academic Field",
        data.students["academic_field"].unique(),
    )

with right:
    students = (
        data.students
        if not selected_academic_field
        else data.students[
            data.students["academic_field"] == selected_academic_field
        ]
    )

    selected_major = entity_selector(
        "Major",
        students["major"].unique(),
    )

display_university_results(
    selected_academic_field,
    selected_major,
    data.students,
    data.institutions,
)


st.subheader("Academic Field and Majors Table")

st.dataframe(
    majors_table(data.students),
    width="stretch",
)
