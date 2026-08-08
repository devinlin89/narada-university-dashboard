import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from dashboard.data.transforms import (
    count_by,
    sum_by,
)
from dashboard.visualization.charts import (
    PRIMARY_HEIGHT,
    horizontal_bar_chart,
)
from dashboard.visualization.theme import style_figure


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
        is_primary=True,
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
        is_primary=True,
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
        is_primary=True,
    )


def overview_program_type_chart(
    students_df: pd.DataFrame,
) -> go.Figure:
    """Create a horizontal bar chart of program types."""

    data = count_by(
        students_df,
        column="program_type",
    ).sort_values("student_count")

    return horizontal_bar_chart(
        data,
        x="student_count",
        y="program_type",
        tick_distance=5,
        wrap_width=28,
        is_primary=True,
    )


def overview_domestic_donut_chart(
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


def overview_jabodetabek_donut_chart(
    students_df: pd.DataFrame,
) -> go.Figure:
    """Create a donut chart comparing Jabodetabek and non-Jabodetabek students."""

    data = students_df.loc[
        students_df["country"] == "Indonesia",
        "within_jabodetabek",
    ].dropna()

    counts = data.value_counts()

    fig = px.pie(
        names=[
            "Within Jabodetabek",
            "Outside Jabodetabek",
        ],
        values=[
            counts.get(True, 0),
            counts.get(False, 0),
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