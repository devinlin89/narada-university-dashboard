import streamlit as st

from dashboard.data.loader import load_dashboard_data
from dashboard.data.tables import majors_table
from dashboard.ui.cards import page_header
from dashboard.ui.styles import load_css

data = load_dashboard_data()

load_css()

page_header(
    title="Majors",
    description=(
        "Explore the academic fields and majors chosen by the graduating class."
    )
)

st.dataframe(
    majors_table(data.students),
    use_container_width=True,
)