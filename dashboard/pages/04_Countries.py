import streamlit as st

from dashboard.data.loader import load_dashboard_data
from dashboard.data.tables import countries_table
from dashboard.ui.cards import (
    page_header,
    primary_section,
)
from dashboard.ui.styles import load_css
from dashboard.visualization.charts import country_distribution_chart

data = load_dashboard_data()

load_css()

page_header(
    title="Countries",
    description=(
        "Explore where students are studying around the world "
        "and compare destination countries by popularity."
    )
)

with primary_section(
    title="Destination Country Ranking",
    description=(
        "Compare destination countries by the total number of students "
        "studying there."
    ),
):
    st.plotly_chart(
        country_distribution_chart(data.institutions),
        use_container_width=True,
        config={"displayModeBar": False},
    )


st.dataframe(
    countries_table(data.institutions),
    use_container_width=True,
)