from collections import Counter

import pandas as pd

from config.config import DECISION_FACTORS


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