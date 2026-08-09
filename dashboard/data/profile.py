from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True, slots=True)
class UniversityProfile:
    institution: str
    country: str
    students: int

@dataclass(frozen=True, slots=True)
class CountryProfile:
    country: str
    students: int
    universities: int
    academic_fields: int
    majors: int

@dataclass(frozen=True, slots=True)
class ScholarshipStatistics:
    received: int
    no_scholarship: int
    no_response: int


def university_profile(
    selected_institution: str,
    institutions: pd.DataFrame,
    student_count: int | None = None,
) -> UniversityProfile:
    """Return summary information for a selected university."""

    data = institutions.loc[
        institutions["institution"].eq(selected_institution)
    ]

    if student_count is None:
        student_count = int(data["student_count"].sum())

    return UniversityProfile(
        institution=selected_institution,
        country=data["country"].iat[0],
        students=student_count,
    )


def country_profile(
    selected_country: str,
    students_df: pd.DataFrame,
) -> CountryProfile:
    """Return summary information for the selected country."""

    data = students_df.loc[
        students_df["country"] == selected_country
    ]

    return CountryProfile(
            country=data["country"].iat[0],
            students=len(data),
            universities=data["institution"].nunique(),
            academic_fields=data["academic_field"].nunique(),
            majors=data["major"].nunique(),
        )


def scholarship_statistics(
    students_df: pd.DataFrame,
) -> ScholarshipStatistics:
    """Return scholarship statistics for a group of students."""

    responses = students_df["received_scholarship?"]
    counts = responses.value_counts()

    return ScholarshipStatistics(
        received=int(counts.get(True, 0)),
        no_scholarship=int(counts.get(False, 0)),
        no_response=int(responses.isna().sum()),
    )