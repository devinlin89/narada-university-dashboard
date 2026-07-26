import streamlit as st
import plotly.express as px
import pandas as pd

df = pd.DataFrame(columns=["lat", "lon"])

fig = px.scatter_geo(df)

fig.show()