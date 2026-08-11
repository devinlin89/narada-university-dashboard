from aliases.generator import AliasGenerator
from cleaning.pipeline import CleaningPipeline
from config.config import ALIAS_COLUMNS
from institutions.generator import InstitutionGenerator


def main() -> None:
    """Run the complete data processing and generation workflow."""
    CleaningPipeline.run()

    for column in ALIAS_COLUMNS:
        AliasGenerator.run(column)

    InstitutionGenerator.run()


if __name__ == "__main__":
    main()