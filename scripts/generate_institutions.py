from time import perf_counter

import pandas as pd

from common.data_io import load_students
from config.config import INSTITUTIONS_DATA
from config.logger import (
    configure_logging,
    get_logger,
)

logger = get_logger("scripts.generate_institutions")


def generate_institutions(df: pd.DataFrame) -> pd.DataFrame:
    # Generate a unique institutions dataset with student counts

    group_columns = ["institution", "campus", "country"]

    institutions_df = (
        df.groupby(group_columns)
        .size()
        .reset_index(name="student_count")
        .sort_values(group_columns)
        .reset_index(drop=True)
    )

    return institutions_df


def export_data(df: pd.DataFrame) -> None:
    # Export the institution dataset

    INSTITUTIONS_DATA.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(INSTITUTIONS_DATA, index=False)


# Main function 

def main() -> None:
    configure_logging()

    start_time = perf_counter()

    try:
        logger.info("Loading student dataset...")
        df = load_students()

        logger.info("Loaded %d rows.", len(df))

        logger.info("Generating institution dataset...")
        institutions_df = generate_institutions(df)

        logger.info(
            "Generated %d unique institutions.",
            len(institutions_df),
        )

        logger.info("Exporting institution dataset...")
        export_data(institutions_df)

        logger.info(
            "Exported institution dataset to %s.",
            INSTITUTIONS_DATA,
        )

        logger.info("Institution generation completed successfully.")
    
    except Exception:
        logger.exception("Institution generation failed.")
        raise

    finally:
        elapsed = perf_counter() - start_time
        logger.info("Total execution time: %.3f s.", elapsed)


if __name__ == "__main__":
    main()