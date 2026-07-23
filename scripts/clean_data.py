from cleaning.pipeline import CleaningPipeline


def main() -> None:
    # Run the data cleaning pipeline
    CleaningPipeline().run()


if __name__ == "__main__":
    main()