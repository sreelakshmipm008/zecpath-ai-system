import re

# Common resume section headings
SECTION_HEADINGS = [
    "professional summary",
    "summary",
    "profile",
    "objective",
    "experience",
    "work experience",
    "education",
    "skills",
    "technical skills",
    "professional skills",
    "projects",
    "project",
    "certifications",
    "certification",
    "internships",
    "achievements",
    "languages",
    "contact",
    "responsibilities",
    "duration"
]


def normalize_headings(text):
    """
    Normalize common resume section headings.
    """

    for heading in SECTION_HEADINGS:

        pattern = rf"(?im)^\s*{re.escape(heading)}\s*$"

        text = re.sub(
            pattern,
            heading.title(),
            text
        )

    return text


def normalize_bullets(text):
    """
    Replace different bullet symbols with '-'
    """

    bullets = [
        "•",
        "●",
        "▪",
        "◦",
        "►",
        "*",
        "–",
        "—"
    ]

    for bullet in bullets:
        text = text.replace(bullet, "-")

    return text


def clean_text(text):
    """
    Clean and normalize extracted resume text.
    """

    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Normalize bullets
    text = normalize_bullets(text)

    # Remove unwanted special characters
    text = re.sub(r"[^\w\s.,@():/\-&+#]", "", text)

    # Remove extra spaces and tabs
    text = re.sub(r"[ \t]+", " ", text)

    # Remove spaces before/after newlines
    text = re.sub(r" *\n *", "\n", text)

    # Remove multiple blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Normalize section headings
    text = normalize_headings(text)

    return text.strip()