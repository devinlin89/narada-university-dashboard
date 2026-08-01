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
        "Browse all university destinations for the Narada Class of 2026."
    )
)

st.dataframe(
    universities_table(data.institutions),
    use_container_width=True,
)