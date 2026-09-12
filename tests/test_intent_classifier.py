"""
Tests for candidate answer intent classification.
"""

import sys
from pathlib import Path

import pytest

# Add the project root to Python's import path.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from answer_understanding.intent_classifier import IntentClassifier


def test_empty_answer_is_missing():
    classifier = IntentClassifier()

    assert classifier.classify(
        "",
        "Do you have Python experience?"
    ) == "missing"


def test_vague_answer_is_vague():
    classifier = IntentClassifier()

    assert classifier.classify(
        "I don't know.",
        "Do you have Python experience?"
    ) == "vague"


def test_yes_no_answer_to_yes_no_question_is_on_topic():
    classifier = IntentClassifier()

    assert classifier.classify(
        "Yes.",
        "Do you have Python experience?"
    ) == "on_topic"


def test_human_resources_synonym_is_on_topic():
    classifier = IntentClassifier()

    assert classifier.classify(
        "Yes, I have worked in HR for two years.",
        "Do you have professional experience in human resources?"
    ) == "on_topic"


def test_tally_related_answer_is_on_topic():
    classifier = IntentClassifier()

    assert classifier.classify(
        "I have worked with bookkeeping software for several years.",
        "Do you have experience using Tally for accounting tasks?"
    ) == "on_topic"


def test_terraform_related_answer_is_on_topic():
    classifier = IntentClassifier()

    assert classifier.classify(
        "I have worked with infrastructure automation tools.",
        "Do you have experience with Terraform?"
    ) == "on_topic"


def test_patient_care_synonym_is_on_topic():
    classifier = IntentClassifier()

    assert classifier.classify(
        "I enjoy working with patients and healthcare teams.",
        "Do you have professional experience in patient care?"
    ) == "on_topic"


def test_clearly_unrelated_answer_is_off_topic():
    classifier = IntentClassifier()

    assert classifier.classify(
        "I enjoy cooking and photography.",
        "Do you have professional experience with Python?"
    ) == "off_topic"


def test_non_string_answer_raises_type_error():
    classifier = IntentClassifier()

    with pytest.raises(TypeError):
        classifier.classify(
            None,
            "Do you have Python experience?"
        )   