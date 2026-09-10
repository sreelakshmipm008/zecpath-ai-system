"""
Behavioral indicators report generation.

Day 27:
- Combine communication confidence and sentiment analysis results.
- Produce a structured behavioral indicators report.
"""

from __future__ import annotations

from typing import Any


class BehavioralIndicatorsReport:
    """Build a structured report from Day 27 analysis results."""

    def generate(
        self,
        communication_analysis: dict[str, Any],
        sentiment_analysis: dict[str, Any],
    ) -> dict[str, Any]:
        """Generate a behavioral indicators report."""

        if not isinstance(communication_analysis, dict):
            raise TypeError("communication_analysis must be a dictionary")

        if not isinstance(sentiment_analysis, dict):
            raise TypeError("sentiment_analysis must be a dictionary")

        return {
            "hesitation": communication_analysis.get("hesitation", {}),
            "response_length": communication_analysis.get(
                "response_length", {}
            ),
            "response_pace": communication_analysis.get(
                "response_pace", {}
            ),
            "uncertainty": communication_analysis.get(
                "uncertainty", {}
            ),
            "contradictions": communication_analysis.get(
                "contradictions", {}
            ),
            "communication_strength": communication_analysis.get(
                "communication_strength", {}
            ),
            "sentiment": sentiment_analysis.get("sentiment", "neutral"),
            "sentiment_score": sentiment_analysis.get("score", 0.0),
        }