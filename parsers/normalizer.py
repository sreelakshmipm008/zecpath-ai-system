"""
normalizer.py

This module normalizes job description text by cleaning
unnecessary whitespace while preserving the original content.
"""

import re


def normalize_text(text):
    """
    Normalize Job Description text.

    Parameters:
        text (str): Raw job description text.

    Returns:
        str: Normalized text.
    """

    # Remove leading/trailing whitespace
    text = text.strip()

    # Replace multiple spaces/tabs with a single space
    text = re.sub(r"[ \t]+", " ", text)

    # Remove multiple blank lines
    text = re.sub(r"\n\s*\n+", "\n", text)

    return text