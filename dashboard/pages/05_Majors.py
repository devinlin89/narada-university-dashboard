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
        "Explore the majors and academic fields chosen by students "
        "and discover where those programs are offered around the world."
    )
)

st.dataframe(
    majors_table(data.students),
    use_container_width=True,
)   