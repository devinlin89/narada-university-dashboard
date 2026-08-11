import re

import pycountry

from config.config import REFERENCE_DATA

STOP_WORDS = {
    "university",
    "universitas",
    "college",
    "campus",
    "kampus",
    "branch"
}

COUNTRY_NAMES = {
    country.name.lower()
    for country in pycountry.countries
}


def remove_phrases(text: str, phrases: set[str]) -> str:
    """Remove a collection of phrases from a string.

    Args:
        text(str): The input string.
        phrases(set[str]): A set of phrases to remove.

    Returns:
        str: The string with the phrases removed.
    """

    for phrase in sorted(phrases, key=len, reverse=True):
        text = re.sub(re.escape(phrase), "", text, flags=re.IGNORECASE)

    return text


def remove_words(text: str, words: set[str]) -> str:
    """Remove whole words from a string.

    Args:
        text(str): The input string.
        words(set[str]): A set of whole words to remove.

    Returns:
        str: The string with the words removed.
    """

    for word in sorted(words, key=len, reverse=True):
        text = re.sub(rf"\b{re.escape(word)}\b", "", text, flags=re.IGNORECASE)

    return text


def normalize_whitespace(text: str) -> str:
    """Remove redundant punctuation and whitespace.

    Args:
        text(str): The input string.

    Returns:
        str: The normalized string with extra whitespace removed.
    """

    text = re.sub(r"[(),.:/-]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def clean_campus_name(
        campus: object,
        institution_names: set[str]
) -> object:
    """Clean a campus name by removing institution names, generic words,
    and countries/regions.

    Args:
        campus: The campus name to clean.
        institution_names: A set of institution names to remove from the campus string.

    Returns:
        The cleaned campus name, or the original value if it is not a string.
    """

    if not isinstance(campus, str):
        return campus

    campus = remove_phrases(campus, institution_names)
    campus = remove_words(campus, STOP_WORDS)
    campus = remove_words(campus, COUNTRY_NAMES)

    campus = normalize_whitespace(campus)

    # Replace blank campus name with the default value
    if not campus:
        campus = REFERENCE_DATA.default_values["campus"]

    return campus