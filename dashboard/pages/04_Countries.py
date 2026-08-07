import streamlit as st

from dashboard.data.loader import load_dashboard_data
from dashboard.data.profile import (
    country_profile,
    scholarship_statistics,
)
from dashboard.data.tables import countries_table
from dashboard.data.transforms import filter_country
from dashboard.ui.cards import (
    chart_card,
    country_profile_card,
    page_header,
    primary_section,
    vertical_spacer,
)
from dashboard.ui.filters import entity_selector
from dashboard.ui.layout import two_column_layout
from dashboard.ui.styles import load_css
from dashboard.visualization.countries import (
    country_academic_field_distribution_chart,
    country_decision_factors_chart,
    country_distribution_chart,
    country_major_distribution_chart,
    country_scholarship_benefits_chart,
    country_university_distribution_chart,
)

data = load_dashboard_data()

load_css()

page_header(
    title="Countries",
    description=(
        "Explore where students are studying around the world "
        "and compare destination countries by popularity."
    ),
)


with primary_section(
    title="Most Popular Destination Countries",
    description=(
        "Compare destination countries by the total number of students studying there."
    ),
):
    st.plotly_chart(
        country_distribution_chart(data.institutions),
        width="stretch",
        config={"displayModeBar": False},
    )


st.subheader("Country Selector")

selected_country = entity_selector(
    "Country",
    sorted(data.institutions["country"].unique()),
)

if selected_country is None:
    st.info("Select a country to view detailed statistics.")
else:
    profile = country_profile(
        selected_country,
        data.students,
    )

    two_column_layout(
        lambda: country_profile_card(profile),
        lambda: chart_card(
            "University Distribution",
            country_university_distribution_chart(
                selected_country,
                data.institutions,
            ),
        ),
    )

    two_column_layout(
        lambda: chart_card(
            "Academic Field Distribution",
            country_academic_field_distribution_chart(
                selected_country,
                data.students,
            ),
        ),
        lambda: chart_card(
            "Major Distribution",
            country_major_distribution_chart(
                selected_country,
                data.students,
            ),
        ),
    )

    with primary_section(
        title="Decision Factors",
        description=(
            "Reasons students reported for choosing universities in this "
            "country. Students could select multiple factors."
        ),
    ):
        st.plotly_chart(
            country_decision_factors_chart(
                selected_country,
                data.students,
            ),
            width="stretch",
            config={"displayModeBar": False},
        )

    with primary_section(
        title="Scholarships",
        description=(
            "Scholarship participation and the types of financial support "
            "received by students studying in this country."
        ),
    ):
        selected_scholarship_statistics = scholarship_statistics(
            filter_country(
                data.students,
                selected_country,
            )
        )

        vertical_spacer()

        left, middle, right = st.columns(3)

        left.metric("Received Scholarship", selected_scholarship_statistics.received)
        middle.metric("No Response", selected_scholarship_statistics.no_response)
        right.metric("No Scholarship", selected_scholarship_statistics.no_scholarship)

        st.markdown("#### Scholarship Types")

        st.plotly_chart(
            country_scholarship_benefits_chart(
                selected_country,
                data.students,
            ),
            width="stretch",
            config={"displayModeBar": False},
        )


st.subheader("Countries Table")

st.dataframe(
    countries_table(data.institutions),
    width="stretch",
)
