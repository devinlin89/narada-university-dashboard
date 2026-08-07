import pandas as pd
import plotly.graph_objects as go

from dashboard.data.transforms import (
    count_by,
    count_decision_factors,
    count_scholarship_benefits,
    filter_university,
    sum_by,
)
from dashboard.visualization.charts import horizontal_bar_chart


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

    top_universities = (
        data.loc[data["student_count"] > 1]
        .sort_values("student_count")
    )

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
        is_primary=True,
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
        wrap_width=26
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
        tick_distance=2,
        wrap_width=28,
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
    )


def university_decision_factors_chart(
    selected_institution: str,
    students_df: pd.DataFrame,
) -> go.Figure:
    """Create a horizontal bar chart of decision factors for the selected university."""

    data = count_decision_factors(
        filter_university(
            students_df,
            selected_institution,
        )["decision_factors"]
    )

    return horizontal_bar_chart(
        data,
        x="student_count",
        y="decision_factor",
        wrap_width=28,
        tick_distance=2,
        margin_left=190,
        is_primary=True,
    )


def university_scholarship_benefits_chart(
    selected_institution: str,
    students_df: pd.DataFrame,
) -> go.Figure:
    """Create a horizontal bar chart showing scholarships of the selected university."""

    data = count_scholarship_benefits(
        filter_university(
            students_df,
            selected_institution,
        )["scholarship_description"]
    )

    return horizontal_bar_chart(
        data,
        x="student_count",
        y="benefit",
        margin_left=120,
    )