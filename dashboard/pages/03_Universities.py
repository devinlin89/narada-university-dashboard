import streamlit as st

from dashboard.data.loader import load_dashboard_data
from dashboard.data.tables import universities_table
from dashboard.ui.cards import (
    page_header,
    primary_section,
)
from dashboard.ui.styles import load_css
from dashboard.visualization.charts import university_distribution_chart

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


st.dataframe(
    universities_table(data.institutions),
    use_container_width=True,
)