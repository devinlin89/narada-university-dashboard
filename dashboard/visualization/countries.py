import pandas as pd
import plotly.graph_objects as go

from dashboard.data.transforms import (
    count_by,
    count_decision_factors,
    count_scholarship_benefits,
    filter_country,
    sum_by,
)
from dashboard.visualization.charts import horizontal_bar_chart


def country_distribution_chart(
    institutions_df: pd.DataFrame,
) -> go.Figure:
    """Create a horizontal bar chart of destination countries/regions."""

    data = sum_by(
        institutions_df,
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
        is_primary=True,
    )


def country_university_distribution_chart(
    selected_country: str,
    institutions_df: pd.DataFrame,
) -> go.Figure:
    """Create a horizontal bar chart of universities in the selected country/region."""

    data = sum_by(
        filter_country(
            institutions_df,
            selected_country,
        ),
        group="institution",
    ).sort_values("student_count")

    return horizontal_bar_chart(
        data,
        x="student_count",
        y="institution",
        wrap_width=26,
    )


def country_academic_field_distribution_chart(
    selected_country: str,
    students_df: pd.DataFrame,
) -> go.Figure:
    """Create a horizontal bar chart of academic fields
    in the selected country/region."""

    data = count_by(
        filter_country(
            students_df,
            selected_country,
        ),
        column="academic_field",
    ).sort_values("student_count")

    return horizontal_bar_chart(
        data,
        x="student_count",
        y="academic_field",
        tick_distance=2,
        wrap_width=28,
    )


def country_major_distribution_chart(
    selected_country: str,
    students_df: pd.DataFrame,
) -> go.Figure:
    """Create a horizontal bar chart of majors in the selected country/region."""

    data = count_by(
        filter_country(
            students_df,
            selected_country,
        ),
        column="major",
    ).sort_values("student_count")

    return horizontal_bar_chart(
        data,
        x="student_count",
        y="major",
        wrap_width=28,
    )


def country_decision_factors_chart(
    selected_country: str,
    students_df: pd.DataFrame,
) -> go.Figure:
    """Create a horizontal bar chart of decision factors
    for the selected country/region."""

    data = count_decision_factors(
        filter_country(
            students_df,
            selected_country,
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


def country_scholarship_benefits_chart(
    selected_country: str,
    students_df: pd.DataFrame,
) -> go.Figure:
    """Create a horizontal bar chart showing scholarships
    in the selected country/region."""

    data = count_scholarship_benefits(
        filter_country(
            students_df,
            selected_country,
        )["scholarship_description"]
    )

    return horizontal_bar_chart(
        data,
        x="student_count",
        y="benefit",
        margin_left=120,
    )