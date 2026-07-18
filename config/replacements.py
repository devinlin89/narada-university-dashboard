# config/replacements.py

VALUE_MAPPINGS: dict[str, dict[str, str | bool]] = {
    "within_jabodetabek": {
        "Yes, it is within Jabodetabek/Greater Jakarta Area": True,
        "No, it is outside of Jabodetabek/Greater Jakarta Area": False,
    },
    "received_scholarship?": {
        "Yes": True,
        "No": False,
    },
    "academic_field": {
        "Ai": "Computing & Data",
        "None of above": "Other",
    },
    "country": {
        "China (Mainland)": "China",
    },
}

DEFAULT_VALUES: dict[str, str] = {
    "campus": "Not Specified",
}

MAJOR_TO_ACADEMIC_FIELD: dict[str, str] = {
    "Artificial Intelligence": "Computing & Data",
    "Aviation Technique": "Transportation",
    "Food Science and Technology": "Natural Sciences & Mathematics",
}