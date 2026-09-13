"""
AI error and edge-case handling utilities.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ErrorHandlingResult:
    """Result of AI input validation and recovery handling."""

    status: str
    action: str
    message: str
    retry_allowed: bool


class AIErrorHandler:
    """Handle common AI screening input failures safely."""

    MAX_RETRIES = 2

    def handle_missing_answer(
        self,
        retry_count: int = 0,
    ) -> ErrorHandlingResult:
        """Handle a missing candidate answer."""

        if retry_count < self.MAX_RETRIES:
            return ErrorHandlingResult(
                status="missing",
                action="clarify",
                message="Please provide an answer to the question.",
                retry_allowed=True,
            )

        return ErrorHandlingResult(
            status="missing",
            action="fallback",
            message="No answer was provided after the allowed retries.",
            retry_allowed=False,
        )

    def handle_audio_issue(
        self,
        issue: str,
        retry_count: int = 0,
    ) -> ErrorHandlingResult:
        """Handle recoverable audio input issues safely."""

        if retry_count < self.MAX_RETRIES:
            return ErrorHandlingResult(
                status="audio_issue",
                action="retry",
                message=(
                    f"Audio quality issue detected: {issue}. "
                    "Please try recording your answer again."
                ),
                retry_allowed=True,
            )

        return ErrorHandlingResult(
            status="audio_issue",
            action="fallback",
            message=(
                "Audio quality could not be processed reliably "
                "after the allowed retries."
            ),
            retry_allowed=False,
        )

    def handle_background_noise(
        self,
        noise_detected: bool,
        retry_count: int = 0,
    ) -> ErrorHandlingResult:
        """Handle detected background noise safely."""

        if not noise_detected:
            return ErrorHandlingResult(
                status="audio_clean",
                action="continue",
                message="Audio quality is acceptable.",
                retry_allowed=False,
            )

        if retry_count < self.MAX_RETRIES:
            return ErrorHandlingResult(
                status="background_noise",
                action="retry",
                message=(
                    "Background noise may affect audio processing. "
                    "Please move to a quieter environment and try again."
                ),
                retry_allowed=True,
            )

        return ErrorHandlingResult(
            status="background_noise",
            action="fallback",
            message=(
                "Background noise could not be resolved "
                "after the allowed retries."
            ),
            retry_allowed=False,
        )

    def handle(
        self,
        status: str,
        retry_count: int = 0,
    ) -> ErrorHandlingResult:
        """Route an AI edge case to the appropriate recovery action."""

        if status == "missing":
            return self.handle_missing_answer(retry_count)

        if status == "audio_issue":
            return self.handle_audio_issue(
                "poor audio quality",
                retry_count,
            )

        if status == "background_noise":
            return self.handle_background_noise(
                True,
                retry_count,
            )

        return ErrorHandlingResult(
            status="safe",
            action="continue",
            message="Input can continue through the AI flow.",
            retry_allowed=False,
        )

    def handle_unexpected_error(
        self,
        error: Exception,
    ) -> ErrorHandlingResult:
        """Provide a safe fallback for unexpected AI flow errors."""

        return ErrorHandlingResult(
            status="unexpected_error",
            action="fallback",
            message=(
                "The response could not be processed safely. "
                "Please try again later."
            ),
            retry_allowed=False,
        )

    