import pandas as pd


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