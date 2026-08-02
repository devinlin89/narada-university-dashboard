import streamlit as st

from dashboard.data.loader import load_dashboard_data
from dashboard.data.tables import universities_table
from dashboard.ui.cards import page_header
from dashboard.ui.styles import load_css

data = load_dashboard_data()

load_css()

page_header(
    title="Universities",
    description=(
        "Browse every university destination, compare student counts, and "
        "explore the campuses chosen by the graduating class."
    )
)

st.dataframe(
    universities_table(data.institutions),
    use_container_width=True,
)