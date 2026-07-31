import streamlit as st

from dashboard.data.loader import load_dashboard_data
from dashboard.ui.styles import load_css
from dashboard.visualization.map import world_map

data = load_dashboard_data()

load_css()

st.title("World University Map")

st.plotly_chart(world_map(data.institutions), 
    use_container_width=True,
    config={
        "scrollZoom": True
    }
)