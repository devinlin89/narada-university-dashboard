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
            landcolor="#fafaf8",
            showcountries=True,
            showocean=True,
            oceancolor="#d4dadc",
            countrycolor="#f3eaea",
            showcoastlines=False,
            showframe=False,
            lataxis_showgrid=False,
            lonaxis_showgrid=False,
        )

    fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            height=385  ,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )

    return fig


def overview_country_bar_chart(
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
        height=350,
        xaxis_title="Students",
        yaxis_title=None,
    )

    return style_figure(fig)


def overview_university_bar_chart(
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
        height=350,
        xaxis_title="Students",
        yaxis_title=None,
        margin=dict(l=180, r=20, t=20, b=20),
    )

    return style_figure(fig)


def overview_academic_field_chart(
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
        height=350,
        xaxis_title="Students",
        yaxis_title=None,
    )

    return style_figure(fig)


def overview_domestic_pie_chart(
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


def university_distribution_chart(
    institutions_df: pd.DataFrame,
) -> tuple[go.Figure, list[str]]:
    """
    Create a horizontal bar chart of universities with more than one student.
    Universities chosen by exactly one student are omitted from the chart and
    returned separately.
    """

    data = (
        institutions_df
        .groupby("institution", as_index=False)["student_count"]
        .sum()
        .sort_values("student_count", ascending=False)
    )

    # Universities with multiple students
    major = (
        data[data["student_count"] > 1]
        .sort_values("student_count")
        .copy()
    )

    # Universities chosen by exactly one student
    other = (
        data[data["student_count"] == 1]
        .sort_values("institution")
    )

    other_universities = other["institution"].tolist()

    major["institution"] = major["institution"].apply(
        lambda name: "<br>".join(fill(name, width=26).splitlines())
    )

    fig = px.bar(
        major,
        x="student_count",
        y="institution",
        orientation="h",
        text="student_count",
    )

    fig.update_traces(
        textposition="outside",
        cliponaxis=False,
    )

    fig.update_yaxes(
        title=None,
        categoryorder="array",
        categoryarray=major["institution"].tolist(),
    )

    fig.update_layout(
        xaxis_title="Students",
        margin=dict(l=210, r=40, t=20, b=20),
        height=max(250, 70 + 60 * len(major)),
    )

    return style_figure(fig), other_universities


def country_distribution_chart(
    institutions: pd.DataFrame,
) -> go.Figure:
    """Create a horizontal bar chart of destination countries."""

    data = (
        institutions
        .groupby("country", as_index=False)["student_count"]
        .sum()
        .sort_values("student_count")
    )

    data["country"] = data["country"].apply(
        lambda name: "<br>".join(fill(name, width=20).splitlines())
    )

    fig = px.bar(
        data,
        x="student_count",
        y="country",
        orientation="h",
        text="student_count",
    )

    fig.update_traces(
        textposition="outside",
        cliponaxis=False,
    )

    fig.update_yaxes(
        title=None,
        categoryorder="array",
        categoryarray=data["country"].tolist(),
    )

    fig.update_layout(
        xaxis_title="Students",
        margin=dict(l=160, r=40, t=20, b=20),
        height=max(350, 70 + 60 * len(data)),
    )

    return style_figure(fig)


def academic_field_distribution_chart(
    students: pd.DataFrame,
) -> go.Figure:
    """Create a horizontal bar chart of academic fields."""

    data = (
        students
        .groupby("academic_field", as_index=False)
        .size()
        .rename(columns={"size": "student_count"})
        .sort_values("student_count")
    )

    fig = px.bar(
        data,
        x="student_count",
        y="academic_field",
        orientation="h",
        text="student_count",
    )

    fig.update_traces(
        textposition="outside",
        cliponaxis=False,
    )

    fig.update_yaxes(
        title=None,
        categoryorder="array",
        categoryarray=data["academic_field"].tolist(),
    )

    fig.update_layout(
        xaxis_title="Students",
        margin=dict(l=160, r=40, t=20, b=20),
        height=max(350, 70 + 60 * len(data)),
    )

    return style_figure(fig)