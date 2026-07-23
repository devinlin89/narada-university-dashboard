from aliases.generator import AliasGenerator


def main() -> None:
    # Generate TODO alias tables
    AliasGenerator().run()


if __name__ == "__main__":
    main()