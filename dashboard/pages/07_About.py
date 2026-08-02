import streamlit as st

from dashboard.data.loader import load_dashboard_data
from dashboard.ui.cards import page_header
from dashboard.ui.styles import load_css

data = load_dashboard_data()

load_css()

page_header(
    title="About",
    description=(
        "Learn about the Narada University Dashboard, "
        "its data sources, methodology, and the technologies used to build it."
    )
)

st.write("In progress...")