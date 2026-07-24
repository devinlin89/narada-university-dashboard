from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True, slots=True)
class Coordinate:
    latitude: float
    longitude: float

    def __post_init__(self):
        if not -90 <= self.latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90.")

        if not -180 <= self.longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180.")


@dataclass(frozen=True, slots=True)
class GeocodingTarget:
    institution: str
    campus: str
    country: str

    @classmethod
    def from_row(cls, row: object) -> Self:
        return cls(
            institution=row.institution,
            campus=row.campus,
            country=row.country,
        )   