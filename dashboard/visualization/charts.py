from textwrap import fill

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from dashboard.visualization.theme import style_figure


def map_preview(institutions_df):
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
            fitbounds="locations",
            showland=True,
            landcolor="rgb(250,250,250)",
            showcountries=True,
            showocean=True,
            oceancolor="rgb(0, 104, 201)",
            countrycolor="rgb(214, 214, 216)",
            showcoastlines=False,
            showframe=False,
            lataxis_showgrid=False,
            lonaxis_showgrid=False,
        )

    fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            height=350,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
    return fig


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

    return style_figure(fig)


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
        lambda name: "<br>".join(fill(name, width=24).splitlines())
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

    return style_figure(fig)


def academic_field_chart(
    students_df: pd.DataFrame,
    top_n: int = 5,
) -> go.Figure:
    """Create a horizontal bar chart of academic fields."""

    field_counts = (
        students_df
        .groupby("academic_field")
        .size()
        .reset_index(name="students")
        .sort_values("students", ascending=False)
        .head(top_n)
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

    return style_figure(fig)


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
    )

    fig.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=20, b=20),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.1,
            xanchor="center",
            x=0.5,
        )
    )

    fig.update_traces(
        rotation=180.5,
        hole=0.55,
    )

    return style_figure(fig)