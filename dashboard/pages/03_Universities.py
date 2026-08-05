import streamlit as st

from dashboard.data.loader import load_dashboard_data
from dashboard.data.profile import university_profile
from dashboard.data.tables import universities_table
from dashboard.ui.cards import (
    chart_card,
    page_header,
    primary_section,
    university_profile_card,
)
from dashboard.ui.filters import entity_selector
from dashboard.ui.layout import two_column_layout
from dashboard.ui.styles import load_css
from dashboard.visualization.charts import (
    university_academic_field_distribution_chart,
    university_campus_distribution_chart,
    university_distribution_chart,
    university_major_distribution_chart,
)

data = load_dashboard_data()

load_css()

page_header(
    title="Universities",
    description=(
        "Browse every university destination, compare student counts, and "
        "explore the campuses chosen by the graduating class."
    )
)


fig, other_universities = university_distribution_chart(data.institutions)

with primary_section(
    title="Most Popular University Destinations",
    description=(
        "Compare universities by total student count across all campuses. "
        "Universities chosen by only one student are summarized below."
    ),
):
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False},
    )

    st.info(
        f"Note: **{len(other_universities)}** additional universities "
        "were each chosen by one student. Expand the section below to view "
        "the complete list."
    )

    with st.expander("View these universities"):
        st.markdown(
            "\n".join(f"- {name}" for name in other_universities)
        )

selected_university = entity_selector(
    "University",
    data.institutions["institution"].unique(),
)

if selected_university is None:
    st.info("Select a university to view detailed statistics.")
else:
    selected_university_profile = university_profile(
        selected_university,
        data.institutions,
    )

    two_column_layout(
        lambda: university_profile_card(
            selected_university_profile,
        ),
        lambda: chart_card(
            "Campus Distribution",
            university_campus_distribution_chart(
                selected_university,
                data.institutions,
            ),
        ),
    )

    two_column_layout(
        lambda: chart_card(
            "Academic Field Distribution",
            university_academic_field_distribution_chart(
                selected_university,
                data.students,
            ),
        ),
        lambda: chart_card(
            "Major Distribution",
            university_major_distribution_chart(
                selected_university,
                data.students,
            ),
        ),
    )


st.subheader("Universities Table")

st.dataframe(
    universities_table(data.institutions),
    use_container_width=True,
)