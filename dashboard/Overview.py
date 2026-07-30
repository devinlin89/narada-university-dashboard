import streamlit as st

from dashboard.data.loader import load_dashboard_data
from dashboard.ui.overview import (
    did_you_know,
    metric_grid,
    supporting_charts,
)
from dashboard.ui.styles import load_css
from dashboard.visualization.charts import map_preview

data = load_dashboard_data()

load_css()

st.title("🎓 Narada University Dashboard")

st.write(
    "Explore the university destinations of the Naradanian Class of 2026. "
    "Browse admissions statistics, universities, majors, and destination countries."
)

# ==========================
# Summary Metrics
# ==========================

metric_grid(data.statistics)

# ==========================
# Map Preview
# ==========================

map_preview(data.institutions)

# ==========================
# Two-column charts
# ==========================

supporting_charts(data)

# ==========================
# Interesting Facts
# ==========================

did_you_know(data.statistics)