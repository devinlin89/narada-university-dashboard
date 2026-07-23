import pandas as pd

from cleaning.stages import (
    CLEANING_PIPELINE,
    PipelineStage,
)
from cleaning.validation import validate_dataset
from common.data_io import load_raw_data
from common.pipeline import Pipeline
from config.config import (
    PROCESSED_DATA_DIR,
    STUDENTS_DATA,
)
from config.logger import get_logger


def export_data(df: pd.DataFrame) -> None:
    # Save the cleaned dataset CSV file

    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(STUDENTS_DATA, index=False)


# Data Cleaning Pipeline Class

class CleaningPipeline(Pipeline):
    # Run the complete student data cleaning workflow

    logger = get_logger("cleaning.pipeline")

    stages: tuple[PipelineStage, ...] = CLEANING_PIPELINE

    @classmethod
    def execute(cls) -> None:
        logger = cls.logger

        logger.info("Loading raw dataset...")
        df = load_raw_data()

        logger.info("Loaded %d rows.", len(df))

        df = cls.run_stages(df)

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

    @classmethod
    def run_stages(cls, df: pd.DataFrame) -> pd.DataFrame:
        # Run the configured cleaning stages

        for message, stage in cls.stages:
            cls.logger.info(message)
            df = stage(df)

        return df