import streamlit as st
import plotly.express as px
import pandas as pd

def create_map(df=None):
    if df is None:
        df = pd.DataFrame({'lat': [], 'lon': []})  # Example data

    fig = px.scatter_mapbox(
        df, 
        lat='lat', 
        lon='lon', 
        zoom=1, 
        color_discrete_sequence=["red"]
        )

    fig.update_layout(
        mapbox_style="open-street-map",
        width=1000,
        height=600,
        margin=dict(l=0, r=0, t=0, b=0),
    )
    return fig