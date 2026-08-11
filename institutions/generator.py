import pandas as pd

from common.data_io import load_students
from common.pipeline import Pipeline
from config.config import INSTITUTIONS_DATA
from config.logger import get_logger


def build_institutions(df: pd.DataFrame) -> pd.DataFrame:
    """Build the institution dataset from the student dataset.

    Each unique combination of institution, campus, and country is grouped
    together and assigned a student count.

    Args:
        df (pd.DataFrame): Student dataset used to generate institution data.

    Returns:
        pd.DataFrame: Institution dataset containing institution, campus,
            country, and student count columns.
    """

    group_columns = ["institution", "campus", "country"]

    return (
        df.groupby(group_columns)
        .size()
        .reset_index(name="student_count")
        .sort_values(group_columns)
        .reset_index(drop=True)
    )


def export_institutions(df: pd.DataFrame) -> None:
    """Export the institution dataset.

    Args:
        df (pd.DataFrame): DataFrame containing institution dataset to export.
    """

    INSTITUTIONS_DATA.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(INSTITUTIONS_DATA, index=False)


class InstitutionGenerator(Pipeline):
    """Generate the institution dataset from the student dataset."""

    logger = get_logger("institutions.generator")

    @classmethod
    def execute(cls) -> None:
        """Build and export the institution dataset."""

        logger = cls.logger

        logger.info("Loading student dataset...")
        df = load_students()

        logger.info("Loaded %d rows.", len(df))

        logger.info("Generating institution dataset...")
        institutions_df = build_institutions(df)

        logger.info(
            "Generated %d unique institutions.",
            len(institutions_df),
        )

        logger.info("Exporting institution dataset...")
        export_institutions(institutions_df)

        logger.info(
            "Exported institution dataset to %s.",
            INSTITUTIONS_DATA,
        )

        logger.info("Institution generation completed successfully.")