from collections import Counter

import pandas as pd
import plotly.graph_objects as go

from config.config import (
    DECISION_FACTORS,
    SCHOLARSHIP_TYPES,
)
from dashboard.data.transforms import count_by
from dashboard.visualization.charts import (
    VERTICAL_BAR_HEIGHT,
    horizontal_bar_chart,
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


def decision_factors_chart(
    students_df: pd.DataFrame,
) -> go.Figure:
    """Create a horizontal bar chart of university decision factors."""

    factors = Counter()

    for factor_list in students_df["decision_factors"]:
        factors.update(factor_list)

    data = pd.DataFrame(
        {
            "decision_factor": DECISION_FACTORS,
            "student_count": [
                factors[factor]
                for factor in DECISION_FACTORS
            ],
        }
    )

    other_count = sum(
        count
        for factor, count in factors.items()
        if factor not in DECISION_FACTORS
    )

    if other_count:
        data.loc[len(data)] = {
            "decision_factor": "Other",
            "student_count": other_count,
        }

    data = data.sort_values("student_count")

    return horizontal_bar_chart(
        data,
        x="student_count",
        y="decision_factor",
        wrap_width=28,
        tick_distance=2,
        margin_left=190,
        is_primary=True
    )


def scholarship_benefits_chart(
    students_df: pd.DataFrame,
) -> go.Figure:
    """Create a horizontal bar chart of scholarship benefits."""

    descriptions = (
        students_df["scholarship_description"]
        .dropna()
        .str.lower()
    )

    counts = Counter()

    for description in descriptions:
        for benefit, keywords in SCHOLARSHIP_TYPES.items():
            if any(keyword in description for keyword in keywords):
                counts[benefit] += 1

    data = (
        pd.DataFrame(
            counts.items(),
            columns=["benefit", "student_count"],
        )
        .sort_values("student_count")
    )

    return horizontal_bar_chart(
        data,
        x="student_count",
        y="benefit",
        tick_distance=2,
        margin_left=120,
        is_primary=True,
    )