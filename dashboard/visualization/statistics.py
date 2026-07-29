from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class DashboardStatistics:
    # Headline metrics
    total_students: int
    total_universities: int
    total_countries: int
    total_fields: int

    # Chart data
    country_counts: pd.DataFrame
    field_counts: pd.DataFrame

    # Insight cards
    most_popular_university: str
    most_popular_country: str
    most_popular_field: str
    domestic_students: int
    international_students: int

    @classmethod
    def from_data(
        cls,
        students_df: pd.DataFrame,
        institutions_df: pd.DataFrame,
    ) -> "DashboardStatistics":

        country_counts = (
            institutions_df
            .groupby("country", as_index=False)["student_count"]
            .sum()
            .sort_values("student_count")
        )

        field_counts = (
            students_df
            .groupby("academic_field")
            .size()
            .reset_index(name="students")
            .sort_values("students")
        )

        domestic_students = (
            students_df["country"]
            .eq("Indonesia")
            .sum()
        )

        international_students = (
            len(students_df) - domestic_students
        )

        return cls(
            total_students=len(students_df),
            total_universities=len(institutions_df),
            total_countries=institutions_df["country"].nunique(),
            total_fields=students_df["academic_field"].nunique(),

            country_counts=country_counts,
            field_counts=field_counts,

            most_popular_university=(
                institutions_df
                .sort_values("student_count", ascending=False)
                .iloc[0]["institution"]
            ),

            most_popular_country=(
                country_counts.iloc[-1]["country"]
            ),

            most_popular_field=(
                field_counts.iloc[-1]["academic_field"]
            ),

            domestic_students=domestic_students,
            international_students=international_students,
        )