from aliases.pipeline import AliasProcessor


def main() -> None:
    # Run the alias pipeline to apply configured aliases
    AliasProcessor().run()


if __name__ == "__main__":
    main()