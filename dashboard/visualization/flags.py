import pycountry

from config.config import COUNTRY_FLAG_NAMES


def country_flag(country: str) -> str:
    """Return the flag emoji for a country/region name."""

    flag_country = COUNTRY_FLAG_NAMES.get(country, country)

    try:
        code = pycountry.countries.lookup(flag_country).alpha_2
    except LookupError:
        return "🌍"

    return "".join(
        chr(ord("🇦") + ord(letter) - ord("A"))
        for letter in code
    )