import streamlit as st

from dashboard.data.loader import load_dashboard_data
from dashboard.data.tables import admissions_table
from dashboard.ui.cards import page_header
from dashboard.ui.styles import load_css

data = load_dashboard_data()

load_css()

page_header(
    title="Admissions",
    description=(
        "Explore how many universities students applied to, the offers they "
        "received, and their scholarship outcomes understand the "
        "admissions outcomes of the Class of 2026."
    )
)

st.dataframe(
    admissions_table(data.students),
    use_container_width=True,
)