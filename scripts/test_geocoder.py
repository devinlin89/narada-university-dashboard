from geocoding.geocoder import (
    build_query,
    create_geocoder,
    geocode,
)

geocoder = create_geocoder()

query = build_query(
    institution="The Chinese University of Hong Kong",
    campus="Shenzhen",
    country="China",
)

print(query)

coordinates = geocode(geocoder, query)

print(coordinates)

