import streamlit as st
import plotly.express as px
import pandas as pd

def create_map(df: pd.DataFrame):
    fig = px.scatter_geo(df, lat='lat', lon='lon')
    return fig