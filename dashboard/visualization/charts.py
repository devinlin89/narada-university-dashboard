from collections import Counter
from textwrap import fill

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from config.config import SCHOLARSHIP_TYPES
from dashboard.visualization.theme import style_figure

# Height constants for charts

CARD_HEIGHT = 250
PRIMARY_HEIGHT = 350
MAP_HEIGHT = 385


def map_preview(institutions_df: pd.DataFrame) -> go.Figure:
    """Create a world map preview of university destinations."""

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
        height=MAP_HEIGHT,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig


def horizontal_bar_chart(
    data: pd.DataFrame,
    *,
    x: str,
    y: str,
    x_title: str = "Students",
    wrap_width: int | None = None,
    tick_distance: int = 1,
    margin_left: int = 210,
    height: int = 250,
) -> go.Figure:
    """Create a standardized horizontal bar chart."""

    if wrap_width:
        data = data.copy()
        data[y] = data[y].apply(
            lambda text: "<br>".join(fill(text, width=wrap_width).splitlines())
        )

    fig = px.bar(
        data,
        x=x,
        y=y,
        orientation="h",
        text=x,
    )

    fig.update_traces(
        textposition="outside",
        cliponaxis=False,
    )

    fig.update_xaxes(
        title=x_title,
        dtick=tick_distance,
        tickmode="linear",
        rangemode="tozero",
    )

    fig.update_yaxes(
        title=None,
        categoryorder="array",
        categoryarray=data[y].tolist(),
    )

    fig.update_layout(
        margin=dict(
            l=margin_left,
            r=40,
            t=20,
            b=20,
        ),
        height=height,
    )

    return style_figure(fig)


def vertical_bar_chart(
    data: pd.DataFrame,
    *,
    x: str,
    y: str,
    x_title: str | None = None,
    y_title: str = "Students",
    x_tick_distance: int = 1,
    y_tick_distance: int = 1,
    height: int = 450,
) -> go.Figure:
    """Create a standardized vertical bar chart."""

    fig = px.bar(
        data,
        x=x,
        y=y,
        text=y,
    )

    fig.update_traces(
        textposition="outside",
        cliponaxis=False,
    )

    fig.update_xaxes(
        title=x_title,
        dtick=x_tick_distance,
    )

    fig.update_yaxes(
        title=y_title,
        dtick=y_tick_distance,
        tickmode="linear",
        rangemode="tozero",
    )

    fig.update_layout(
        margin=dict(
            l=40,
            r=40,
            t=20,
            b=20,
        ),
        height=height,
    )

    return style_figure(fig)


def filter_university(
    data: pd.DataFrame,
    institution: str,
) -> pd.DataFrame:
    """Return rows for a single university."""

    return data.loc[data["institution"] == institution]


def count_by(
    data: pd.DataFrame,
    *,
    column: str,
) -> pd.DataFrame:
    """Count the number of students by a given column."""

    return (
        data.groupby(column, as_index=False)
        .size()
        .rename(columns={"size": "student_count"})
    )


def sum_by(
    data: pd.DataFrame,
    *,
    group: str,
    value: str = "student_count",
) -> pd.DataFrame:
    """Sum the number of students by a given column."""

    return data.groupby(group, as_index=False)[value].sum()


def overview_country_bar_chart(
    institutions_df: pd.DataFrame,
) -> go.Figure:
    """Create a horizontal bar chart of destination countries."""

    data = sum_by(institutions_df, group="country").sort_values("student_count")

    return horizontal_bar_chart(
        data,
        x="student_count",
        y="country",
        wrap_width=20,
        tick_distance=5,
        margin_left=160,
        height=PRIMARY_HEIGHT,
    )


def overview_university_bar_chart(
    institutions_df: pd.DataFrame,
    top_n: int = 5,
) -> go.Figure:
    """Create a horizontal bar chart of the most popular universities."""

    data = (
        sum_by(institutions_df, group="institution")
        .sort_values("student_count", ascending=False)
        .head(top_n)
        .sort_values("student_count")
    )

    return horizontal_bar_chart(
        data,
        x="student_count",
        y="institution",
        wrap_width=24,
        tick_distance=2,
        margin_left=180,
        height=PRIMARY_HEIGHT,
    )


def overview_academic_field_chart(
    students_df: pd.DataFrame,
    top_n: int = 5,
) -> go.Figure:
    """Create a horizontal bar chart of academic fields."""

    data = (
        count_by(
            students_df,
            column="academic_field",
        )
        .sort_values("student_count", ascending=False)
        .head(top_n)
        .sort_values("student_count")
    )

    return horizontal_bar_chart(
        data,
        x="student_count",
        y="academic_field",
        tick_distance=5,
        wrap_width=28,
        height=PRIMARY_HEIGHT,
    )


def overview_domestic_pie_chart(
    students_df: pd.DataFrame,
) -> go.Figure:
    """Create a donut chart comparing domestic and international students."""

    domestic = students_df["country"].eq("Indonesia").sum()

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
        height=PRIMARY_HEIGHT,
        margin=dict(l=20, r=20, t=20, b=20),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.1,
            xanchor="center",
            x=0.5,
        ),
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

    data = sum_by(institutions_df, group="institution").sort_values(
        "student_count", ascending=False
    )

    top_universities = data.loc[data["student_count"] > 1].sort_values("student_count")

    other_universities = (
        data.loc[data["student_count"] == 1]
        .sort_values("institution")["institution"]
        .tolist()
    )

    fig = horizontal_bar_chart(
        top_universities,
        x="student_count",
        y="institution",
        wrap_width=26,
        height=PRIMARY_HEIGHT,
    )

    return fig, other_universities


def university_campus_distribution_chart(
    selected_institution: str,
    institutions_df: pd.DataFrame,
) -> go.Figure:
    """Create a horizontal bar chart of campuses for the selected university."""

    data = filter_university(
        institutions_df,
        selected_institution,
    ).sort_values("student_count")

    return horizontal_bar_chart(
        data,
        x="student_count",
        y="campus",
        wrap_width=26,
        height=CARD_HEIGHT,
    )


def university_academic_field_distribution_chart(
    selected_institution: str,
    students_df: pd.DataFrame,
) -> go.Figure:
    """Create a horizontal bar chart of academic fields for the selected university."""

    data = count_by(
        filter_university(students_df, selected_institution),
        column="academic_field",
    ).sort_values("student_count")

    return horizontal_bar_chart(
        data,
        x="student_count",
        y="academic_field",
        wrap_width=28,
        height=CARD_HEIGHT,
    )


def university_major_distribution_chart(
    selected_institution: str,
    students_df: pd.DataFrame,
) -> go.Figure:
    """Create a horizontal bar chart of majors for the selected university."""

    data = count_by(
        filter_university(
            students_df,
            selected_institution,
        ),
        column="major",
    ).sort_values("student_count")

    return horizontal_bar_chart(
        data,
        x="student_count",
        y="major",
        wrap_width=28,
        height=CARD_HEIGHT,
    )


def university_decision_factors_chart(
    selected_institution: str,
    students_df: pd.DataFrame,
) -> go.Figure:
    """Create a horizontal bar chart of decision factors for the selected university."""

    factors = Counter()

    for factor_list in filter_university(
        students_df,
        selected_institution,
    )["decision_factors"]:
        factors.update(factor_list)

    data = pd.DataFrame(
        factors.items(),
        columns=["decision_factor", "student_count"],
    ).sort_values("student_count")

    return horizontal_bar_chart(
        data,
        x="student_count",
        y="decision_factor",
        wrap_width=28,
        margin_left=190,
        height=PRIMARY_HEIGHT,
    )


def university_scholarship_benefits_chart(
    selected_institution: str,
    students_df: pd.DataFrame,
) -> go.Figure:
    """Create a horizontal bar chart showing scholarship benefits."""

    descriptions = (
        filter_university(
            students_df,
            selected_institution,
        )["scholarship_description"]
        .dropna()
        .str.lower()
    )

    counts = Counter()

    for description in descriptions:
        for benefit, keywords in SCHOLARSHIP_TYPES.items():
            if any(keyword in description for keyword in keywords):
                counts[benefit] += 1

    data = pd.DataFrame(
        counts.items(),
        columns=["benefit", "student_count"],
    ).sort_values("student_count")

    return horizontal_bar_chart(
        data,
        x="student_count",
        y="benefit",
        margin_left=120,
        height=CARD_HEIGHT,
    )


def country_distribution_chart(
    institutions: pd.DataFrame,
) -> go.Figure:
    """Create a horizontal bar chart of destination countries."""

    data = sum_by(
        institutions,
        group="country",
        value="student_count",
    ).sort_values("student_count")

    return horizontal_bar_chart(
        data,
        x="student_count",
        y="country",
        wrap_width=20,
        tick_distance=5,
        margin_left=160,
        height=PRIMARY_HEIGHT,
    )


def academic_field_distribution_chart(
    students: pd.DataFrame,
) -> go.Figure:
    """Create a horizontal bar chart of academic fields."""

    data = count_by(
        students,
        column="academic_field",
    ).sort_values("student_count")

    return horizontal_bar_chart(
        data,
        x="student_count",
        y="academic_field",
        tick_distance=5,
        margin_left=160,
        height=max(PRIMARY_HEIGHT, 70 + 60 * len(data)),
    )


def applications_distribution_chart(
    students: pd.DataFrame,
) -> go.Figure:
    """Create a bar chart of the number of university applications."""

    data = (
        count_by(
            students,
            column="applications_count",
        )
        .sort_values("applications_count")
    )

    return vertical_bar_chart(
        data,
        x="applications_count",
        y="student_count",
        x_title="Universities Applied To",
        y_tick_distance=2,
        height=450,
    )