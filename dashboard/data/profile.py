from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class UniversityProfile:
    institution: str
    country: str
    students: int

@dataclass(frozen=True)
class ScholarshipStatistics:
    received: int
    no_scholarship: int
    no_response: int


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


def scholarship_statistics(
    selected_institution: str,
    students_df: pd.DataFrame,
) -> ScholarshipStatistics:
    """Return scholarship statistics for the selected university."""

    data = students_df.loc[
        students_df["institution"] == selected_institution
    ]

    responses = data["received_scholarship?"]
    counts = responses.value_counts()

    return ScholarshipStatistics(
        received=int(counts.get(True, 0)),
        no_scholarship=int(counts.get(False, 0)),
        no_response=int(responses.isna().sum()),
    )