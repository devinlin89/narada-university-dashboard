import pandas as pd
import plotly.graph_objects as go

from dashboard.data.transforms import count_by
from dashboard.visualization.charts import (
    VERTICAL_BAR_HEIGHT,
    vertical_bar_chart,
)


def applications_distribution_chart(students_df: pd.DataFrame) -> go.Figure:
    """Create a bar chart of the number of university applications."""

    data = (
        count_by(
            students_df,
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
        height=VERTICAL_BAR_HEIGHT,
    )


def offers_distribution_chart(students_df: pd.DataFrame) -> go.Figure:
    """Create a bar chart of the number of university offers."""

    data = (
        count_by(
            students_df,
            column="acceptances_count",
        )
        .sort_values("acceptances_count")
    )

    return vertical_bar_chart(
        data,
        x="acceptances_count",
        y="student_count",
        x_title="Offers Received",
        y_tick_distance=2,
        height=VERTICAL_BAR_HEIGHT,
    )