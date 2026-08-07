from dataclasses import dataclass
from math import asin, cos, radians, sin, sqrt

import pandas as pd

from geocoding.models import Coordinate

# Coordinates of Jakarta
JAKARTA = (-6.2000, 106.8167)

def haversine(
    origin: Coordinate,
    destination: Coordinate,
) -> float:
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lat1, lon1 = map(radians, origin)
    lat2, lon2 = map(radians, destination)

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Determines return value units.

    return c * r


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
    farthest_destination: str
    domestic_students: int
    international_students: int

    # Admissions metrics
    average_applications: float
    average_offer_rate: float
    received_scholarship: int

    @classmethod
    def from_data(
        cls,
        students_df: pd.DataFrame,
        institutions_df: pd.DataFrame,
    ) -> "DashboardStatistics":
        """Create dashboard statistics from student and institution data."""

        # Chart Data

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


        # Insight Cards

        institutions = institutions_df.copy()

        institutions["distance_km"] = institutions.apply(
            lambda row: haversine(
                JAKARTA,
                (row["latitude"], row["longitude"]),
            ),
            axis=1,
        )

        farthest = institutions.loc[
            institutions["distance_km"].idxmax()
        ]


        domestic_students = (
            students_df["country"]
            .eq("Indonesia")
            .sum()
        )

        international_students = (
            len(students_df) - domestic_students
        )


        # Admission Metrics

        average_applications = students_df["applications_count"].mean()

        offer_rates = students_df["acceptances_count"].div(
            students_df["applications_count"].replace(0, pd.NA)
        )

        average_offer_rate = offer_rates.mean()

        received_scholarship = (
            students_df["received_scholarship?"].eq(True).sum()
        )

        return cls(
            total_students=len(students_df),
            total_universities=institutions_df["institution"].nunique(),
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
            farthest_destination=farthest['institution'],
            domestic_students=domestic_students,
            international_students=international_students,

            average_applications=average_applications,
            average_offer_rate=average_offer_rate,
            received_scholarship=received_scholarship,
        )