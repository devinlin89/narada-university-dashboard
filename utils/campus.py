# utils/campus.py

import re

import pycountry

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
    # Remove a collection of phrases from a string

    for phrase in sorted(phrases, key=len, reverse=True):
        text = re.sub(re.escape(phrase), "", text, flags=re.IGNORECASE)

    return text


def remove_words(text: str, words: set[str]) -> str:
    # Remove whole words from a string

    for word in sorted(words, key=len, reverse=True):
        text = re.sub(rf"\b{re.escape(word)}\b", "", text, flags=re.IGNORECASE)

    return text


def normalize_whitespace(text: str) -> str:
    # Remove redundant punctuation and whitespace

    text = re.sub(r"[(),.:/-]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def clean_campus_name(
        campus: object,
        institution_names: set[str]
) -> object:
    # Remove institution names, generic words, and countries from a campus name

    if not isinstance(campus, str):
        return campus

    campus = remove_phrases(campus, institution_names)
    campus = remove_words(campus, STOP_WORDS)
    campus = remove_words(campus, COUNTRY_NAMES)

    campus = normalize_whitespace(campus)

    # Replaces blank campus name
    if not campus:
        campus = "Not Specified"

    return campus