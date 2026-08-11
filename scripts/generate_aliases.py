from aliases.generator import AliasGenerator
from common.cli import parse_alias_column_args


def main() -> None:
    """Generate TODO Aliases."""

    args = parse_alias_column_args(
        "Generate TODO alias files from processed data.",
    )

    AliasGenerator.run(args.column)


if __name__ == "__main__":
    main()