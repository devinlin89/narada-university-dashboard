import pandas as pd
import plotly.graph_objects as go

from dashboard.visualization.charts import (
    PRIMARY_HEIGHT,
    count_by,
    horizontal_bar_chart,
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