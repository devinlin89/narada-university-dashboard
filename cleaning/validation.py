import pandas as pd

from validation.validators import (
    validate_aliases,
    validate_boolean_columns,
    validate_list_columns,
    validate_required_fields,
)


def validate_dataset(df: pd.DataFrame) -> None:
    # Validate the cleaned dataset before export

    validate_required_fields(df)
    validate_boolean_columns(df)
    validate_list_columns(df)
    validate_aliases(df)