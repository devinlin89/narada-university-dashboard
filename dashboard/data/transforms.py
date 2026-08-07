from collections import Counter

import pandas as pd

from config.config import (
    DECISION_FACTORS,
    SCHOLARSHIP_TYPES,
)


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
    other_count = 0

    for factor_list in decision_factors:
        factors.update(
            factor
            for factor in factor_list
            if factor in valid_factors
        )

        other_count += sum(
            factor not in valid_factors
            for factor in factor_list
        )

    if other_count:
        factors["Other"] = other_count

    return (
        pd.DataFrame(
            factors.items(),
            columns=["decision_factor", "student_count"],
        )
        .sort_values("student_count")
    )


def count_scholarship_benefits(
    descriptions: pd.Series,
) -> pd.DataFrame:
    """Count scholarship benefits from scholarship descriptions."""

    counts = Counter()

    for description in descriptions.dropna().str.lower():
        for benefit, keywords in SCHOLARSHIP_TYPES.items():
            if any(keyword in description for keyword in keywords):
                counts[benefit] += 1

    return (
        pd.DataFrame(
            counts.items(),
            columns=["benefit", "student_count"],
        )
        .sort_values("student_count")
    )