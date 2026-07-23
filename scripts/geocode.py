from geocoding.pipeline import CoordinateGenerator


def main() -> None:
    # Run the geocoding coordinate generation pipeline
    CoordinateGenerator().run()


if __name__ == "__main__":
    main()