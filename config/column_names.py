COLUMN_MAPPING = {
    "Timestamp": "timestamp",
    """Please check the box below to confirm that:
- I am a Narada School Grade 12 student from the Class of 2026, and
- my final post-graduation destination has been officially confirmed, and
- I have committed to attending it.""": "requirements_met",
    "Name": "name",
    "Class": "class",
    "What type of academic/professional program or pathway are you attending next?": "program_type",
    "What university/institution are you attending next?": "institution",
    "If the university/institution has multiple campuses/branches, enter the campus/branch you are attending.": "campus",
    "Is this university / institution / destination within Jabodetabek/Greater Jakarta Area?": "within_jabodetabek",
    "What city is this university / institution / destination located in?": "city",
    "What country is this university / institution / destination located in?": "country",
    "What specific major/program are you planning or intending to study?": "major",
    "Which broader academic field does your major most closely align with?": "academic_field",
    "Approximately how many universities/institutions did you apply to or select during the admissions process?": "applications_count",
    "How many acceptances/offers did you receive?": "acceptances_count",
    "Did you receive any type of scholarship or financial aid offer to your committed destination? (Optional)": "received_scholarship?",
    "Describe the scholarship or financial aid offered at your committed destination. (Optional)": "scholarship_description",
    "What factors most influenced your post-graduation destination decision?": "decision_factors",
    "Thoughts about your destination or program? (Optional)": "additional_comments",
    "Are you okay with your anonymized data being used for this project?": "consent"
}


DROPPED_COLUMNS = ["timestamp", "requirements_met", "name", "class", "consent"]