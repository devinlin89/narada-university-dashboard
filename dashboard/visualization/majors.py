import pandas as pd
import plotly.graph_objects as go

from dashboard.data.transforms import (
    count_by,
)
from dashboard.visualization.charts import horizontal_bar_chart


def academic_field_distribution_chart(
    students_df: pd.DataFrame,
) -> go.Figure:
    """Create a horizontal bar chart of academic fields."""

    data = count_by(
        students_df,
        column="academic_field",
    ).sort_values("student_count")

    return horizontal_bar_chart(
        data,
        x="student_count",
        y="academic_field",
        wrap_width=28,
        tick_distance=5,
        margin_left=160,
        is_tall=True,
    )


def major_country_distribution_chart(
    students_df: pd.DataFrame,
) -> go.Figure:
    """Create a horizontal bar chart of destination countries."""

    data = (
        count_by(
            students_df,
            column="country",
        )
        .sort_values("student_count")
    )

    return horizontal_bar_chart(
        data,
        x="student_count",
        y="country",
        wrap_width=20,
        tick_distance=2,
        margin_left=160,
    )