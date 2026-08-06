import streamlit as st

from dashboard.data.loader import load_dashboard_data
from dashboard.data.profile import (
    scholarship_statistics,
    university_profile,
)
from dashboard.data.tables import universities_table
from dashboard.ui.cards import (
    chart_card,
    page_header,
    primary_section,
    university_profile_card,
    vertical_spacer,
)
from dashboard.ui.filters import entity_selector
from dashboard.ui.layout import two_column_layout
from dashboard.ui.styles import load_css
from dashboard.visualization.universities import (
    university_academic_field_distribution_chart,
    university_campus_distribution_chart,
    university_decision_factors_chart,
    university_distribution_chart,
    university_major_distribution_chart,
    university_scholarship_benefits_chart,
)

data = load_dashboard_data()

load_css()

page_header(
    title="Universities",
    description=(
        "Browse every university destination, compare student counts, and "
        "explore the campuses chosen by the graduating class."
    ),
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
        width="stretch",
        config={"displayModeBar": False},
    )

    st.info(
        f"Note: **{len(other_universities)}** additional universities "
        "were each chosen by one student. Expand the section below to view "
        "the complete list."
    )

    with st.expander("View these universities"):
        st.markdown("\n".join(f"- {name}" for name in other_universities))


st.subheader("University Selector")

selected_university = entity_selector(
    "University/Institution",
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


    with primary_section(
        title="Decision Factors",
        description=(
            "Reasons students reported for choosing this university. "
            "Students could select multiple factors."
        ),
    ):
        st.plotly_chart(
            university_decision_factors_chart(
                selected_university,
                data.students,
            ),
            width="stretch",
            config={"displayModeBar": False},
        )


    with primary_section(
        title="Scholarships",
        description=(
            "Understand scholarship participation and the types of "
            "financial support received by students attending this university."
        ),
    ):
        selected_scholarship_statistics = scholarship_statistics(
            selected_university,
            data.students,
        )

        vertical_spacer()

        left, middle, right = st.columns(3)

        left.metric("Received Scholarship", selected_scholarship_statistics.received)
        middle.metric("No Response", selected_scholarship_statistics.no_response)
        right.metric("No Scholarship", selected_scholarship_statistics.no_scholarship)

        st.markdown("#### Scholarship Types")

        st.plotly_chart(
            university_scholarship_benefits_chart(
                selected_university,
                data.students,
            ),
            width="stretch",
            config={"displayModeBar": False},
        )


st.subheader("Universities Table")

st.dataframe(
    universities_table(data.institutions),
    width="stretch",
)
