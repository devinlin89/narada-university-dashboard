
import streamlit as st

from dashboard.data.loader import load_dashboard_data
from dashboard.ui.cards import (
    chart_card,
    metric_card,
)
from dashboard.visualization.charts import (
    academic_field_chart,
    country_bar_chart,
    domestic_pie_chart,
    map_preview,
    university_bar_chart,
)

data = load_dashboard_data()

st.title("🎓 Narada University Dashboard")
st.caption("University Destinations of the Naradanian Class of 2026")

st.write(
    "Explore the university destinations of the Narada graduating class. "
    "Browse admissions statistics, universities, majors, and countries."
)

# ==========================
# Summary Metrics
# ==========================

col1, col2, col3, col4 = st.columns(4)

with col1:
    metric_card("Students", data.statistics.total_students)

with col2:
    metric_card("Universities", data.statistics.total_universities)

with col3:
    metric_card("Countries", data.statistics.total_countries)

with col4:
    metric_card("Academic Fields", data.statistics.total_fields)

# ==========================
# Map Preview
# ==========================

map_preview(data.institutions)

# ==========================
# Two-column charts
# ==========================

left, right = st.columns(2)

with left:
    chart_card(
        "Top Destination Countries",
        country_bar_chart(data.institutions),
    )

with right:
    chart_card(
        "Top Universities",
        university_bar_chart(data.institutions),
    )

left, right = st.columns(2)

with left:
    chart_card(
        "Academic Fields",
        academic_field_chart(data.students),
    )

with right:
    chart_card(
        "Domestic vs International",
        domestic_pie_chart(data.students),
    )

# ==========================
# Interesting Facts
# ==========================

st.subheader("Did You Know?")

...