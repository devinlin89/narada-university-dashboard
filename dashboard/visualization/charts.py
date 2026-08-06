from textwrap import fill

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from dashboard.visualization.theme import style_figure

# Height constants for charts

MIN_CARD_HEIGHT = 240
MAX_CARD_HEIGHT = 600
PRIMARY_HEIGHT = 350
VERTICAL_BAR_HEIGHT = 450
MAP_PREVIEW_HEIGHT = 385
WORLD_MAP_HEIGHT = 500

def chart_height(
    rows: int,
    *,
    threshold: int = 4,
) -> int:
    """Return the appropriate chart height based on the number of rows."""

    return MAX_CARD_HEIGHT if rows > threshold else MIN_CARD_HEIGHT


def horizontal_bar_chart(
    data: pd.DataFrame,
    *,
    x: str,
    y: str,
    x_title: str = "Students",
    wrap_width: int | None = None,
    tick_distance: int = 1,
    margin_left: int = 210,
    is_primary: bool = False,
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

    if is_primary:
        height = PRIMARY_HEIGHT
    else:
        height = chart_height(len(data))

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


def filter_country(
    data: pd.DataFrame,
    country: str,
) -> pd.DataFrame:
    """Return rows for a single destination country."""

    return data.loc[data["country"] == country]


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
