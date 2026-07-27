import streamlit as st
from visualization.map import create_map
import pandas as pd

st.title("World University Map")

fig = create_map()

st.plotly_chart(fig, 
    use_container_width=True,
    config={
        "scrollZoom": True
    }
)