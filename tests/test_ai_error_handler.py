import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from utils.ai_error_handler import AIErrorHandler

def test_missing_answer_requests_clarification():
    handler = AIErrorHandler()

    result = handler.handle("missing")

    assert result.status == "missing"
    assert result.action == "clarify"
    assert result.retry_allowed is True


def test_audio_issue_requests_retry():
    handler = AIErrorHandler()

    result = handler.handle("audio_issue")

    assert result.status == "audio_issue"
    assert result.action == "retry"
    assert result.retry_allowed is True


def test_background_noise_requests_retry():
    handler = AIErrorHandler()

    result = handler.handle("background_noise")

    assert result.status == "background_noise"
    assert result.action == "retry"
    assert result.retry_allowed is True


def test_unknown_status_continues_safely():
    handler = AIErrorHandler()

    result = handler.handle("unknown")

    assert result.status == "safe"
    assert result.action == "continue"
    assert result.retry_allowed is False


def test_unexpected_error_uses_safe_fallback():
    handler = AIErrorHandler()

    result = handler.handle_unexpected_error(
        ValueError("test error")
    )

    assert result.status == "unexpected_error"
    assert result.action == "fallback"
    assert result.retry_allowed is False


def test_retry_limit_triggers_fallback():
    handler = AIErrorHandler()

    result = handler.handle(
        "missing",
        retry_count=handler.MAX_RETRIES,
    )

    assert result.action == "fallback"
    assert result.retry_allowed is False