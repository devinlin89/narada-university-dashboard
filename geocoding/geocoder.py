# utils/geocoder.py
# WARN: STILL BROKEN

from collections.abc import Callable
from random import randint
from time import sleep
from typing import TypeAlias

from geopy.geocoders import Nominatim
from geopy.location import Location

from aliases.tables import get_aliases
from config.config import (
    GEOCODING_OVERRIDES,
    settings,
)

Coordinates: TypeAlias = tuple[float, float]


def create_geocoder() -> Nominatim:
    # Create and configure a Nominatim geocoder

    return Nominatim(
        user_agent=settings.geocoder.user_agent, 
        timeout=settings.geocoder.timeout
    )


def build_queries(
    institution: str,
    campus: str,
    country: str,
) -> list[str]:
    # Build progressively broader geocoding queries.

    queries: list[str] = []

    # Manual override (highest priority)
    override = (
        GEOCODING_OVERRIDES
        .get(institution, {})
        .get(campus)
    )
    if override is not None:
        queries.append(override)

    # Try every institution alias with the campus
    aliases = get_aliases("institution", institution)

    if campus != "Not Specified":
        queries.append(f"{institution}, {campus}, {country}")
        queries.append(f"{institution} {campus}, {country}")

        for alias in aliases:
            queries.append(f"{alias}, {campus}, {country}")
            queries.append(f"{alias} {campus}, {country}")

    # Institution + country
    queries.append(f"{institution}, {country}")

    for alias in aliases:
        queries.append(f"{alias}, {country}")

    # Institution only
    queries.append(institution)

    for alias in aliases:
        queries.append(alias)

    # Campus + country only (last resort)
    if campus != "Not Specified":
        queries.append(f"{campus}, {country}")

    # Remove duplicates while preserving order.
    return list(dict.fromkeys(queries))


def query_geocoder(
    geocoder: Nominatim,
    query: str,
) -> Location | None:
    # Execute a single geocoding request while respecting the rate limit.

    try:
        return geocoder.geocode(query)
    finally:
        # Always wait, even if geopy raises an exception.
        sleep(randint(2, 5))


def geocode(
    geocoder: Nominatim,
    institution: str,
    campus: str,
    country: str,
    log: Callable[[str], None] | None = None,
) -> tuple[float, float] | None:
    # Geocode an institution using progressively broader queries.

    queries = build_queries(
        institution,
        campus,
        country,
    )

    for query in queries:
        if log is not None:
            log(f"Searching: {query}")

        location = query_geocoder(
            geocoder,
            query,
        )

        if location is None:
            continue

        if log is not None:
            log(f"Found: {location.address}")

        return (
            location.latitude,
            location.longitude,
        )

    if log is not None:
        log("Location not found.")

    return None
