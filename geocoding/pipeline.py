import pandas as pd
from geopy.geocoders import Nominatim

from common.data_io import (
    load_coordinates,
    load_institutions,
)
from common.pipeline import Pipeline
from config.config import COORDINATES_DATA
from config.logger import get_logger
from geocoding.finder import find_missing_locations
from geocoding.geocoder import (
    create_geocoder,
    geocode,
)
from geocoding.models import (
    Coordinate,
    GeocodingTarget,
)

logger = get_logger("geocoding.pipeline") 

def geocode_row(
    geocoder: Nominatim,
    target: GeocodingTarget,
) -> dict[str, object] | None:
    # Geocode a single institution

    coordinate: Coordinate | None = geocode(
        geocoder,
        target,
        log=logger.info,
    )

    if coordinate is None:
        return None

    return {
        "institution": target.institution,
        "campus": target.campus,
        "country": target.country,
        "latitude": coordinate.latitude,
        "longitude": coordinate.longitude,
    }


def geocode_locations(
    geocoder: Nominatim,
    locations_df: pd.DataFrame,
) -> pd.DataFrame:
    # Geocode a collection of institution locations

    new_rows: list[dict[str, object]] = []

    total = len(locations_df)

    for index, row in enumerate(
        locations_df.itertuples(index=False),
        start=1,
    ):
        target = GeocodingTarget.from_row(row)

        logger.info(
            "[%d/%d] %s, %s, %s",
            index,
            total,
            target.institution,
            target.campus,
            target.country
        )

        result = geocode_row(
            geocoder,
            target,
        )

        if result is not None:
            new_rows.append(result)
        
    return pd.DataFrame(new_rows)


def update_coordinates(
    coordinates_df: pd.DataFrame,
    new_coordinates_df: pd.DataFrame,
) -> pd.DataFrame:
    # Append newly geocoded locations to the coordinate cache

    return (
        pd.concat(
            [coordinates_df, new_coordinates_df],
            ignore_index=True,
        )
        .sort_values(
            ["country", "institution", "campus"]
        )
    )


def export_coordinates(df: pd.DataFrame) -> None:
    # Export the institution coordinate dataset.

    COORDINATES_DATA.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        COORDINATES_DATA,
        index=False,
    )


class CoordinateGenerator(Pipeline):
    # Generate coordinates for institutions

    logger = logger
    
    @classmethod
    def execute(cls) -> None:
        logger = cls.logger

        geocoder = create_geocoder()

        logger.info("Loading institution dataset...")
        institutions_df = load_institutions()

        logger.info(
            "Loaded %d unique institutions.",
            len(institutions_df),
        )

        logger.info("Loading coordinate cache...")
        coordinates_df = load_coordinates()
        logger.info(
            "Loaded %d cached coordinates.",
            len(coordinates_df),
        )

        logger.info("Finding missing locations...")
        missing_locations = find_missing_locations(
            institutions_df,
            coordinates_df,
        )

        logger.info(
            "Found %d locations requiring geocoding.",
            len(missing_locations),
        )

        logger.info("Geocoding missing locations...")
        new_coordinates_df = geocode_locations(
            geocoder,
            missing_locations,
        )

        logger.info(
            "Successfully geocoded %d new locations.",
            len(new_coordinates_df),
        )

        logger.info("Updating coordinate cache...")
        updated_coordinates_df = update_coordinates(
            coordinates_df,
            new_coordinates_df,
        )

        logger.info("Exporting coordinate cache...")
        export_coordinates(updated_coordinates_df)

        logger.info(
            "Exported %d coordinates to %s.",
            len(updated_coordinates_df),
            COORDINATES_DATA,
        )

        logger.info("Geocoding completed successfully.")