import streamlit as st
import plotly.express as px
import pandas as pd

def create_map(df: pd.DataFrame):
    fig = px.scatter_geo(df, lat='lat', lon='lon')

    fig.update_layout(
    margin=dict(l=100, r=100, t=100, b=100)
    )
    return fig