from collections import Counter

import pandas as pd

from config.config import DECISION_FACTORS


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


def count_decision_factors(
    decision_factors: pd.Series,
) -> pd.DataFrame:
    """Count valid decision factors from a series of factor lists."""

    valid_factors = set(DECISION_FACTORS)

    factors = Counter()

    for factor_list in decision_factors:
        factors.update(
            factor
            for factor in factor_list
            if factor in valid_factors
        )

    return (
        pd.DataFrame(
            factors.items(),
            columns=["decision_factor", "student_count"],
        )
        .sort_values("student_count")
    )