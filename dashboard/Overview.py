from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from config.config import (
    COORDINATES_DATA,
    INSTITUTIONS_DATA,
    STUDENTS_DATA,
)


@st.cache_data
def load_csv(file_path: Path) -> pd.DataFrame:
    return pd.read_csv(file_path)


students_df = load_csv(STUDENTS_DATA)
institutions_df = load_csv(INSTITUTIONS_DATA)
coordinates_df = load_csv(COORDINATES_DATA)

institutions_df = institutions_df.merge(
        coordinates_df,
        on=["institution", "campus", "country"],
        how="left",
        validate="one_to_one",
    )

st.set_page_config(
    page_title="Narada University Dashboard",
    page_icon="🎓",
    layout="wide",
)

st.title("🎓 Narada University Dashboard")
st.caption("University Destinations • Class of 2026")

st.write(
    """
    Explore the university destinations of the Narada graduating class.
    Use the navigation sidebar to browse different analyses.
    """
)

# --------------------------------------------------------
# KPI Cards
# --------------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Students",
    len(students_df),
)

col2.metric(
    "Universities",
    institutions_df["institution"].nunique(),
)

col3.metric(
    "Countries",
    institutions_df["country"].nunique(),
)

col4.metric(
    "Academic Fields",
    students_df["academic_field"].nunique(),
)

st.divider()

# --------------------------------------------------------
# World Map Preview
# --------------------------------------------------------

st.markdown("## 🌍 University Destinations")

fig = px.scatter_geo(
    institutions_df,
    lat="latitude",
    lon="longitude",
    size="student_count",
    projection="equirectangular",
)

fig.update_traces(
    marker=dict(
        color="red",
        line=dict(width=0),
    ),
    hoverinfo="skip",
    hovertemplate=None,
)

fig.update_geos(
    showland=True,
    landcolor="rgb(250, 250, 250)",
    showocean=True,
    oceancolor="rgb(0, 123, 186)",
    countrycolor="white",
    showcoastlines=False,
    showframe=False,
    lataxis_showgrid=False,
    lonaxis_showgrid=False,
    fitbounds=False,
)

fig.update_layout(
    margin=dict(l=0, r=0, t=0, b=0),
    height=450,
)

st.plotly_chart(
    fig,
    use_container_width=True,
    config={
        "displayModeBar": False,
        "staticPlot": True,
    },
)

if st.button(
    "🌍 Explore Interactive Map",
    use_container_width=True,
):
    st.switch_page("pages/02_World_Map.py")

# --------------------------------------------------------
# Supporting Charts
# --------------------------------------------------------

country_counts = (
    institutions_df
    .groupby("country", as_index=False)["student_count"]
    .sum()
    .sort_values("student_count")
)

field_counts = (
    students_df
    .groupby("academic_field")
    .size()
    .reset_index(name="students")
    .sort_values("students")
)

left, right = st.columns(2)

with left:

    st.subheader("Top Destination Countries")

    fig = px.bar(
        country_counts,
        x="student_count",
        y="country",
        orientation="h",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

with right:

    st.subheader("Top Universities")

    fig = px.bar(
        institutions_df.sort_values("student_count"),
        x="student_count",
        y="institution",
        orientation="h",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

left, right = st.columns(2)

with left:

    st.subheader("Academic Fields")

    fig = px.bar(
        field_counts,
        x="students",
        y="academic_field",
        orientation="h",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

with right:

    st.subheader("Domestic vs International")

    domestic = (
        students_df["country"]
        .eq("Indonesia")
        .sum()
    )

    international = len(students_df) - domestic

    fig = px.pie(
        names=[
            "Domestic",
            "International",
        ],
        values=[
            domestic,
            international,
        ],
        hole=0.5,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

st.divider()

# --------------------------------------------------------
# Did You Know?
# --------------------------------------------------------

st.subheader("Did You Know?")

left, right = st.columns(2)

with left:

    st.info(
        f"🏛️ **Most Popular University**\n\n"
        f"{institutions_df.sort_values(
            'student_count', ascending=False
        ).iloc[0]['institution']}"
    )

    st.info(
        f"🌍 **Most Popular Country**\n\n"
        f"{country_counts.iloc[-1]['country']}"
    )

with right:

    st.info(
        f"🎓 **Most Popular Academic Field**\n\n"
        f"{field_counts.iloc[-1]['academic_field']}"
    )

    st.info(
        f"🌎 **Countries Represented**\n\n"
        f"{institutions_df['country'].nunique()}"
    )