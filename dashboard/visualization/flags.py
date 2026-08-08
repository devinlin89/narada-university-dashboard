import pycountry


def country_flag(country: str) -> str:
    """Return the flag emoji for a country name."""

    try:
        code = pycountry.countries.lookup(country).alpha_2
    except LookupError:
        return "🌍"

    return "".join(
        chr(ord("🇦") + ord(letter) - ord("A"))
        for letter in code
    )