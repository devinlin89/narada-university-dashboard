import streamlit as st

from dashboard.data.loader import load_dashboard_data
from dashboard.data.profile import university_profile
from dashboard.data.tables import majors_table
from dashboard.ui.cards import (
    page_header,
    primary_section,
    university_profile_card,
)
from dashboard.ui.filters import entity_selector, universities_by_major
from dashboard.ui.layout import metric_row
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

st.subheader("Major Selector")

selected_major = entity_selector(
    "Major",
    data.students["major"].unique(),
)

if selected_major is None:
    st.info("Select a major to see the universities students in that major applied to.")
else:
    metric_row(
        (
            "Total Students",
            len(data.students[data.students["major"] == selected_major])
        ),
        (
            "Most Common Country",
            (
                data.students[data.students["major"] == selected_major]["country"]
                .mode()[0]
            )
        ),
    )
    universities = universities_by_major(
    selected_major,
    data.students,
)
    universities_profiles = []
    for university in universities:
        profile = university_profile(
            university,
            data.institutions,)
        universities_profiles.append(profile)

    for i in range(0, len(universities_profiles), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(universities_profiles):
                with cols[j]:
                    university_profile_card(universities_profiles[i + j])


st.dataframe(
    majors_table(data.students),
    width="stretch",
)
