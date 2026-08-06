from collections import Counter

import pandas as pd
import plotly.graph_objects as go

from config.config import SCHOLARSHIP_TYPES
from dashboard.visualization.charts import (
    CARD_HEIGHT,
    PRIMARY_HEIGHT,
    count_by,
    filter_university,
    horizontal_bar_chart,
    sum_by,
)


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
