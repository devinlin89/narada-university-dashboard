import pandas as pd
import plotly.graph_objects as go

from dashboard.visualization.charts import (
    PRIMARY_HEIGHT,
    horizontal_bar_chart,
    sum_by,
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
