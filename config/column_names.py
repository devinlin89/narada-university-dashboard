# config/column_names.py

REQUIREMENTS_QUESTION = """Please check the box below to confirm that:
- I am a Narada School Grade 12 student from the Class of 2026, and
- my final post-graduation destination has been officially confirmed, and
- I have committed to attending it."""

PROGRAM_TYPE_QUESTION = (
    "What type of academic/professional program or pathway "
    "are you attending next?"
)

INSTITUTION_QUESTION = (
    "What university/institution are you attending next?"
)

CAMPUS_QUESTION = (
    "If the university/institution has multiple campuses/branches, "
    "enter the campus/branch you are attending."
)

WITHIN_JABODETABEK_QUESTION = (
    "Is this university / institution / destination "
    "within Jabodetabek/Greater Jakarta Area?"
)

CITY_QUESTION = (
    "What city is this university / institution / destination located in?"
)

COUNTRY_QUESTION = (
    "What country is this university / institution / destination located in?"
)

MAJOR_QUESTION = (
    "What specific major/program are you planning or intending to study?"
)

ACADEMIC_FIELD_QUESTION = (
    "Which broader academic field does your major most closely align with?"
)

APPLICATIONS_QUESTION = (
    "Approximately how many universities/institutions did "
    "you apply to or select during the admissions process?"
)

ACCEPTANCES_QUESTION = (
    "How many acceptances/offers did you receive?"
)

RECEIVED_SCHOLARSHIP_QUESTION = (
    "Did you receive any type of scholarship or financial aid "
    "offer to your committed destination? (Optional)"
)

SCHOLARSHIP_DESCRIPTION_QUESTION = (
    "Describe the scholarship or financial aid offered "
    "at your committed destination. (Optional)"
)

DECISION_FACTORS_QUESTION = (
    "What factors most influenced your post-graduation destination decision?"
)

THOUGHTS_QUESTION = (
    "Thoughts about your destination or program? (Optional)"
)

CONSENT_QUESTION = (
    "Are you okay with your anonymized data being used for this project?"
)

COLUMN_MAPPING = {
    "Timestamp": "timestamp",
    REQUIREMENTS_QUESTION: "requirements_met",
    "Name": "name",
    "Class": "class",
    PROGRAM_TYPE_QUESTION: "program_type",
    INSTITUTION_QUESTION: "institution",
    CAMPUS_QUESTION: "campus",
    WITHIN_JABODETABEK_QUESTION: "within_jabodetabek",
    CITY_QUESTION: "city",
    COUNTRY_QUESTION: "country",
    MAJOR_QUESTION: "major",
    ACADEMIC_FIELD_QUESTION: "academic_field",
    APPLICATIONS_QUESTION: "applications_count",
    ACCEPTANCES_QUESTION: "acceptances_count",
    RECEIVED_SCHOLARSHIP_QUESTION: "received_scholarship?",
    SCHOLARSHIP_DESCRIPTION_QUESTION: "scholarship_description",
    DECISION_FACTORS_QUESTION: "decision_factors",
    THOUGHTS_QUESTION: "additional_comments",
    CONSENT_QUESTION: "consent"
}

DROPPED_COLUMNS = [
    "timestamp",
    "requirements_met",
    "name",
    "class",
    "consent",
    "city"
]

FREE_RESPONSE_COLUMNS = [
    "institution",
    "campus",
    "major",
    "scholarship_description"
]

LIST_RESPONSE_COLUMNS = [
    "decision_factors"
]

REQUIRED_COLUMNS = (
    "institution",
    "country",
    "major",
    "academic_field",
)

BOOLEAN_COLUMNS = (
    "within_jabodetabek",
    "received_scholarship?",
)