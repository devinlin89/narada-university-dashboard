from geocoding.pipeline import GeocodingPipeline


def main() -> None:
    # Run the geocoding coordinate generation pipeline
    GeocodingPipeline().run()


if __name__ == "__main__":
    main()
