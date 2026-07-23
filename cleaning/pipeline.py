from time import perf_counter

import pandas as pd

from cleaning.stages import (
    PIPELINE,
    PipelineStage,
)
from cleaning.validation import validate_dataset
from common.data_io import load_raw_data
from config.config import (
    PROCESSED_DATA_DIR,
    STUDENTS_DATA,
)
from config.logger import (
    configure_logging,
    get_logger,
)

logger = get_logger("cleaning.pipeline")


def export_data(df: pd.DataFrame) -> None:
    # Save the cleaned dataset CSV file

    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(STUDENTS_DATA, index=False)


# Data Cleaning Pipeline Class

class CleaningPipeline:
    # Run the complete student data cleaning workflow

    def __init__(self, stages: tuple[PipelineStage, ...] = PIPELINE):
        self.stages = stages

    def run(self) -> None:
        configure_logging()

        start_time = perf_counter()

        try:
            logger.info("Loading raw dataset...")
            df = load_raw_data()

            logger.info("Loaded %d rows.", len(df))

            df = self.execute_stages(df)

            logger.info("Validating dataset...")
            validate_dataset(df)

            logger.info("Exporting cleaned dataset...")
            export_data(df)

            logger.info(
                "Exported cleaned dataset to %s",
                STUDENTS_DATA,
            )

            logger.info(
                "Dataset summary: %d students, %d institutions, %d majors.",
                len(df),
                df["institution"].nunique(),
                df["major"].nunique(),
            )

            logger.info("Data cleaning completed successfully.")

        except Exception:
            logger.exception("Data cleaning failed.")
            raise

        finally:
            elapsed = perf_counter() - start_time
            logger.info("Total execution time: %.3f s.", elapsed)

    def execute_stages(self, df: pd.DataFrame) -> pd.DataFrame:
        # Run the configured cleaning stages.

        for message, stage in self.stages:
            logger.info(message)
            df = stage(df)

        return df