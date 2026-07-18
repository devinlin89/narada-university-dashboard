from time import perf_counter

import pandas as pd
from geopy.geocoders import Nominatim

from config.logger import (
    configure_logging,
    get_logger,
)
from config.paths import (
    COORDINATES_DATA,
    REFERENCE_DATA_DIR,
)
from utils.data_io import (
    load_coordinates,
    load_institutions,
)
from utils.geocoder import (
    create_geocoder,
    geocode,
)

logger = get_logger("scripts.geocode")


def find_missing_locations(
    institutions_df: pd.DataFrame,
    coordinates_df: pd.DataFrame
) -> pd.DataFrame:
    # Find institutions that have not yet been geocoded

    key_columns = [
        "institution",
        "campus",
        "country",
    ]

    missing = (
        institutions_df
        .merge(
            coordinates_df[key_columns],
            on=key_columns,
            how="left",
            indicator=True,
        )
    )

    return (
        missing.loc[missing["_merge"] == "left_only"]
        .drop(columns="_merge")
        .reset_index(drop=True)
    )


def geocode_row(
    geocoder: Nominatim,
    institution: str,
    campus: str,
    country: str,
) -> dict[str, object] | None:
    # Geocode a single institution

    coordinates = geocode(
        geocoder,
        institution,
        campus,
        country,
        log=logger.info,
    )

    if coordinates is None:
        return None

    latitude, longitude = coordinates

    return {
        "institution": institution,
        "campus": campus,
        "country": country,
        "latitude": latitude,
        "longitude": longitude,
    }


def geocode_locations(
    geocoder: Nominatim,
    locations_df: pd.DataFrame,
) -> pd.DataFrame:
    # Geocode a collection of institution locations

    new_rows: list[dict[str, object]] = []

    total = len(locations_df)

    for index, row in enumerate(
        locations_df.itertuples(),
        start=1,
    ):
        logger.info(
            "[%d/%d] %s, %s",
            index,
            total,
            row.institution,
            row.campus,
        )

        result = geocode_row(
            geocoder,
            row.institution,
            row.campus,
            row.country,
        )

        if result is not None:
            new_rows.append(result)
        
    return pd.DataFrame(new_rows)


def update_coordinates(
    coordinates_df: pd.DataFrame,
    new_coordinates_df: pd.DataFrame,
) -> pd.DataFrame:
    # Append newly geocoded locations to the coordinate cache

    return pd.concat(
        [coordinates_df, new_coordinates_df],
        ignore_index=True,
    )


def export_coordinates(df: pd.DataFrame) -> None:
    # Export the institution coordinate dataset.

    REFERENCE_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        COORDINATES_DATA,
        index=False,
    )


def main() -> None:
    configure_logging()

    start_time = perf_counter()


    try:
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

    except Exception:
        logger.exception("Geocoding failed.")
        raise

    finally:
        elapsed = perf_counter() - start_time
        logger.info("Total execution time: %.3f s.", elapsed)

if __name__ == "__main__":
    main()