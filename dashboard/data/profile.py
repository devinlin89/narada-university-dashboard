from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class UniversityProfile:
    institution: str
    country: str
    students: int

def university_profile(
    selected_institution: str,
    institutions: pd.DataFrame,
) -> UniversityProfile:
    """Return summary information for the selected university."""

    data = institutions.loc[
        institutions["institution"] == selected_institution
    ]

    return UniversityProfile(
        institution=selected_institution,
        country=data["country"].iat[0],
        students=int(data["student_count"].sum()),
    )