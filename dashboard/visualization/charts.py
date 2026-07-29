from textwrap import fill

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def map_preview(institutions_df: pd.DataFrame) -> None:
    """Render the overview world map preview."""

    with st.container(border=True):
        st.subheader("🌍 University Destinations")
        st.caption(
            "Preview of university destinations. "
            "Open the interactive map to explore individual universities."
        )

        fig = px.scatter_geo(
            institutions_df,
            lat="latitude",
            lon="longitude",
            size="student_count",
            projection="equirectangular",
        )

        fig.update_traces(
            marker=dict(
                color="#e2703e",
                line=dict(width=0),
            ),
            hoverinfo="skip",
            hovertemplate=None,
        )

        fig.update_geos(
            showland=True,
            landcolor="rgb(250,250,250)",
            showocean=True,
            oceancolor="rgb(0,123,186)",
            countrycolor="white",
            showcoastlines=False,
            showframe=False,
            lataxis_showgrid=False,
            lonaxis_showgrid=False,
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
            key="explore_map",
            use_container_width=True,
        ):
            st.switch_page("pages/02_World_Map.py")


def country_bar_chart(
    institutions_df: pd.DataFrame,
) -> go.Figure:

    country_counts = (
        institutions_df
        .groupby("country", as_index=False)["student_count"]
        .sum()
        .sort_values("student_count")
    )

    fig = px.bar(
        country_counts,
        x="student_count",
        y="country",
        orientation="h",
        text="student_count",
    )

    fig.update_layout(
        xaxis_title="Students",
        yaxis_title=None,
    )

    fig.update_layout(height=350)

    return fig


def university_bar_chart(
    institutions_df: pd.DataFrame,
    top_n: int = 5,
) -> go.Figure:
    """Create a horizontal bar chart of the most popular universities."""

    data = (
        institutions_df
        .groupby("institution", as_index=False)["student_count"]
        .sum()
        .sort_values("student_count", ascending=False)
        .head(top_n)
        .sort_values("student_count")
    )

    data["institution"] = data["institution"].apply(
        lambda name: "<br>".join(fill(name, width=28).splitlines())
    )

    fig = px.bar(
        data,
        x="student_count",
        y="institution",
        orientation="h",
        text="student_count",
    )

    fig.update_yaxes(
        categoryorder="array",
        categoryarray=data["institution"],
        title=None,
    )

    fig.update_layout(
        xaxis_title="Students",
        yaxis_title=None,
        margin=dict(l=180, r=20, t=20, b=20),
    )

    fig.update_layout(height=350)

    return fig


def academic_field_chart(
    students_df: pd.DataFrame,
) -> go.Figure:
    """Create a horizontal bar chart of academic fields."""

    field_counts = (
        students_df
        .groupby("academic_field")
        .size()
        .reset_index(name="students")
        .sort_values("students")
    )

    field_counts["academic_field"] = field_counts["academic_field"].apply(
        lambda name: "<br>"
        .join(fill(name, width=28)
        .splitlines())
    )

    fig = px.bar(
        field_counts,
        x="students",
        y="academic_field",
        orientation="h",
        text="students",
    )

    fig.update_layout(
        xaxis_title="Students",
        yaxis_title=None,
    )

    fig.update_layout(height=350)

    return fig


def domestic_pie_chart(
    students_df: pd.DataFrame,
) -> go.Figure:
    """Create a donut chart comparing domestic and international students."""

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

    fig.update_layout(height=350)    

    return fig