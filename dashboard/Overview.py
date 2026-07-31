import sys
from pathlib import Path

import streamlit as st

# Allow absolute imports when running Streamlit from dashboard/Overview.py
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dashboard.data.loader import load_dashboard_data  # noqa: E402
from dashboard.ui.cards import vertical_spacer  # noqa: E402
from dashboard.ui.overview import (  # noqa: E402
    did_you_know,
    explore_more,
    metric_grid,
    supporting_charts,
)
from dashboard.ui.styles import load_css  # noqa: E402
from dashboard.visualization.charts import map_preview  # noqa: E402

data = load_dashboard_data()

load_css()

st.set_page_config(
    page_title="Narada University Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🎓 Narada University Dashboard")

st.write(
    "Explore the university destinations of the Naradanian Class of 2026. "
    "Browse admissions statistics, universities, majors, and destination countries."
)

# Summary Metrics
metric_grid(data.statistics)
vertical_spacer()

# Map Preview
map_preview(data.institutions)
vertical_spacer()

# Two-column charts
supporting_charts(data)
vertical_spacer()

# Interesting Facts
did_you_know(data.statistics)
vertical_spacer()

# Explore More
explore_more()