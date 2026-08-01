import streamlit as st

from dashboard.data.loader import load_dashboard_data
from dashboard.ui.cards import page_header
from dashboard.ui.styles import load_css
from dashboard.visualization.map import world_map

data = load_dashboard_data()

load_css()

page_header(
    title="World University Map",
    description=(
        "Explore the destinations of Narada Class of 2026 students "
        "around the world. Hover over a marker on the map to view "
        "the university name, campus, country, and student count."
    )
)

st.plotly_chart(world_map(data.institutions), 
    use_container_width=True,
    config={
        "scrollZoom": True
    }
)