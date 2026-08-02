import streamlit as st

from dashboard.data.loader import load_dashboard_data
from dashboard.data.tables import majors_table
from dashboard.ui.cards import page_header
from dashboard.ui.styles import load_css

data = load_dashboard_data()

load_css()

page_header(
    title="Admissions",
    description=(
        "Explore application count, university offers, and scholarship "
        "statistics to better understand the Class of 2026's admissions journey."
    )
)

st.dataframe(
    majors_table(data.students),
    use_container_width=True,
)