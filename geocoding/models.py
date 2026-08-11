from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True, slots=True)
class Coordinate:
    """Geographic coordinates for a location.

    Attributes:
        latitude (float): Latitude in decimal degrees.
        longitude (float): Longitude in decimal degrees.
    """

    latitude: float
    longitude: float

    def __post_init__(self):
        if not -90 <= self.latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90.")

        if not -180 <= self.longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180.")


@dataclass(frozen=True, slots=True)
class GeocodingTarget:
    """Represent a location to be geocoded.

    Attributes:
        institution (str): Name of the institution.
        campus (str): Name of the campus.
        country (str): Country where the institution is located.
    """

    institution: str
    campus: str
    country: str

    @classmethod
    def from_row(cls, row: object) -> Self:
        """Create a geocoding target from a data row.

        Args:
            row (object): Object containing institution, campus, and country
                attributes.

        Returns:
            Self: Geocoding target created from the row.
        """

        return cls(
            institution=row.institution,
            campus=row.campus,
            country=row.country,
        )