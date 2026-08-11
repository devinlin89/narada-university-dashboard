from dataclasses import fields

import pandas as pd

from geocoding.models import GeocodingTarget

KEY_COLUMNS = tuple(
    field.name
    for field in fields(GeocodingTarget)
)

def find_missing_locations(
    institutions_df: pd.DataFrame,
    coordinates_df: pd.DataFrame
) -> pd.DataFrame:
    """Find institutions that have not yet been geocoded.

    Args:
        institutions_df (pd.DataFrame): DataFrame containing all institutions
            that require geocoding.
        coordinates_df (pd.DataFrame): DataFrame containing institutions that
            have already been geocoded.

    Returns:
        pd.DataFrame: Institutions present in `institutions_df` but not in
            `coordinates_df`, with the index reset.
    """

    missing = (
        institutions_df
        .merge(
            coordinates_df[list(KEY_COLUMNS)],
            on=list(KEY_COLUMNS),
            how="left",
            indicator=True,
        )
    )

    return (
        missing.loc[missing["_merge"] == "left_only"]
        .drop(columns="_merge")
        .reset_index(drop=True)
    )