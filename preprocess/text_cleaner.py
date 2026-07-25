import re

def clean_text(text):
    """
    Clean extracted resume text.
    """

    # Remove extra spaces, tabs and newlines
    text = re.sub(r"\s+", " ", text)

    # Remove unwanted special characters
    text = re.sub(r"[^\w\s.,@()-]", "", text)

    # Remove leading and trailing spaces
    text = text.strip()

    return text