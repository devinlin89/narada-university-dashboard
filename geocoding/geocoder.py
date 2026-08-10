from collections.abc import Callable
from random import randint
from time import sleep

from geopy.geocoders import Nominatim
from geopy.location import Location

from aliases.tables import get_aliases
from config.config import (
    REFERENCE_DATA,
    settings,
)
from geocoding.models import (
    Coordinate,
    GeocodingTarget,
)


def create_geocoder() -> Nominatim:
    # Create and configure a Nominatim geocoder

    return Nominatim(
        user_agent=settings.geocoder.user_agent,
        timeout=settings.geocoder.timeout,
    )


def build_queries(target: GeocodingTarget) -> list[str]:
    # Build progressively broader geocoding queries.

    institution = target.institution
    campus = target.campus
    country = target.country

    queries: list[str] = []

    # Manual override (highest priority)
    override = (
        REFERENCE_DATA.geocoding_overrides
        .get(institution, {})
        .get(campus)
    )
    if override is not None:
        queries.append(override)

    # Try every institution alias with the campus
    aliases = get_aliases("institution", institution)

    if campus != REFERENCE_DATA.default_values["campus"]:
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
    if campus != REFERENCE_DATA.default_values["campus"]:
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
        sleep(
            randint(
                settings.geocoder.min_delay,
                settings.geocoder.max_delay,
            )
        )


def geocode(
    geocoder: Nominatim,
    target: GeocodingTarget,
    log: Callable[[str], object] | None = None,
) -> Coordinate | None:
    # Geocode an institution using progressively broader queries.

    queries = build_queries(target)

    for search_query in queries:
        if log is not None:
            log(f"Searching: {search_query}")

        location = query_geocoder(
            geocoder,
            search_query,
        )

        if location is None:
            continue

        if log is not None:
            log(f"Found: {location.address}")

        return Coordinate(
            location.latitude,
            location.longitude,
        )

    if log is not None:
        log("Location not found.")

    return None