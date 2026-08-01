import streamlit as st

from dashboard.data.loader import load_dashboard_data
from dashboard.data.tables import countries_table
from dashboard.ui.cards import page_header
from dashboard.ui.styles import load_css

data = load_dashboard_data()

load_css()

page_header(
    title="Countries",
    description=(
        "Explore where students are studying around the world "
        "and compare destination countries by popularity."
    )
)

st.dataframe(
    countries_table(data.institutions),
    use_container_width=True,
)