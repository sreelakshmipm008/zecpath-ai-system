"""
Dynamic follow-up logic for adaptive HR interviews.

Detects incomplete or vague candidate responses and provides
response-quality information for the follow-up decision process.
"""

from __future__ import annotations

import re
from typing import Any

from interview_ai.interview_state import InterviewState


class FollowUpEngine:
    """Evaluate candidate responses for adaptive follow-up questioning."""

    def __init__(self) -> None:
        self.vague_phrases = {
            "yes",
            "no",
            "maybe",
            "not sure",
            "i don't know",
            "don't know",
            "okay",
            "fine",
            "good",
            "nothing",
            "none",
            "not much",
            "some",
            "a little",
            "sometimes",
        }

    def analyze_response(
        self,
        response: str,
    ) -> dict[str, Any]:
        """
        Analyze a candidate response for completeness and vagueness.

        Returns structured information used by the adaptive
        follow-up decision logic.
        """
        if not isinstance(response, str):
            raise TypeError("Response must be a string.")

        normalized = response.strip().lower()

        if not normalized:
            return {
                "response": "",
                "is_incomplete": True,
                "is_vague": True,
                "word_count": 0,
                "reason": "missing_response",
            }

        words = re.findall(r"\b[\w'-]+\b", normalized)
        word_count = len(words)

        is_incomplete = word_count < 3
        is_vague = normalized in self.vague_phrases

        reason = None

        if is_incomplete:
            reason = "incomplete_response"
        elif is_vague:
            reason = "vague_response"

        return {
            "response": response.strip(),
            "is_incomplete": is_incomplete,
            "is_vague": is_vague,
            "word_count": word_count,
            "reason": reason,
        }

    def determine_follow_up_trigger(
        self,
        response: str,
    ) -> dict[str, Any]:
        """
        Determine the appropriate follow-up trigger based on
        the candidate's response quality.
        """
        analysis = self.analyze_response(response)

        if analysis["is_vague"]:
            return {
                **analysis,
                "follow_up_required": True,
                "trigger": "example_based",
                "prompt_type": "example_based",
            }

        if analysis["is_incomplete"]:
            return {
                **analysis,
                "follow_up_required": True,
                "trigger": "clarification",
                "prompt_type": "clarification",
            }

        return {
            **analysis,
            "follow_up_required": True,
            "trigger": "deepening",
            "prompt_type": "deepening",
        }

    def determine_difficulty_level(
        self,
        response: str,
    ) -> str:
        """
        Classify a candidate response for adaptive questioning.

        Simple responses require a deeper probe.
        Confident responses require a scenario-based follow-up.
        """
        analysis = self.analyze_response(response)

        if analysis["is_incomplete"] or analysis["is_vague"]:
            return "simple"

        word_count = analysis["word_count"]

        confidence_indicators = {
            "i have",
            "i developed",
            "i implemented",
            "i led",
            "i managed",
            "i designed",
            "i built",
            "i handled",
            "i successfully",
            "my experience",
        }

        normalized = response.strip().lower()

        has_confidence_indicator = any(
            indicator in normalized
            for indicator in confidence_indicators
        )

        if has_confidence_indicator and word_count >= 8:
            return "confident"

        return "simple"

    def is_repetitive_question(
        self,
        question_id: str,
        previous_question_ids: list[str],
    ) -> bool:
        """
        Check whether a question has already been asked
        during the current interview.
        """
        if not isinstance(question_id, str):
            raise TypeError("Question ID must be a string.")

        if not isinstance(previous_question_ids, list):
            raise TypeError("Previous question IDs must be a list.")

        return question_id in previous_question_ids

    def get_conversation_context(
        self,
        state: InterviewState,
    ) -> dict[str, Any]:
        """
        Extract the conversation context required for
        adaptive follow-up decisions.
        """
        if not isinstance(state, InterviewState):
            raise TypeError("State must be an InterviewState instance.")

        previous_question_ids = [
            response.question_id
            for response in state.responses
        ]

        previous_responses = [
            response.response
            for response in state.responses
        ]

        return {
            "session_id": state.session_id,
            "current_question_id": state.current_question_id,
            "current_category": state.current_category,
            "phase": state.phase,
            "question_index": state.question_index,
            "previous_question_ids": previous_question_ids,
            "previous_responses": previous_responses,
            "response_count": len(state.responses),
            "completed": state.completed,
        }

    def build_follow_up_decision(
        self,
        response: str,
        state: InterviewState,
        next_question_id: str | None = None,
    ) -> dict[str, Any]:
        """
        Build the adaptive follow-up decision for a candidate response.
        """
        if not isinstance(response, str):
            raise TypeError("Response must be a string.")

        if not isinstance(state, InterviewState):
            raise TypeError("State must be an InterviewState instance.")

        if next_question_id is not None and not isinstance(
            next_question_id,
            str,
        ):
            raise TypeError("Next question ID must be a string or None.")

        analysis = self.analyze_response(response)
        trigger = self.determine_follow_up_trigger(response)
        difficulty = self.determine_difficulty_level(response)
        context = self.get_conversation_context(state)

        if analysis["is_vague"]:
            follow_up_type = "example_based"
        elif analysis["is_incomplete"]:
            follow_up_type = "clarification"
        elif difficulty == "confident":
            follow_up_type = "scenario_based"
        else:
            follow_up_type = "deepening"

        is_repetitive = False

        if next_question_id is not None:
            is_repetitive = self.is_repetitive_question(
                next_question_id,
                context["previous_question_ids"],
            )

        follow_up_required = not is_repetitive

        return {
            "follow_up_required": follow_up_required,
            "follow_up_type": follow_up_type,
            "trigger": trigger["trigger"],
            "difficulty_level": difficulty,
            "is_repetitive": is_repetitive,
            "current_question_id": context["current_question_id"],
            "current_category": context["current_category"],
            "phase": context["phase"],
        }

    def generate_follow_up_instruction(
        self,
        response: str,
        state: InterviewState,
        next_question_id: str | None = None,
    ) -> dict[str, Any]:
        """
        Generate an adaptive follow-up instruction from the
        decision tree.
        """
        decision = self.build_follow_up_decision(
            response=response,
            state=state,
            next_question_id=next_question_id,
        )

        follow_up_type = decision["follow_up_type"]

        instructions = {
            "clarification": (
                "Ask the candidate to clarify or provide more "
                "specific information about the response."
            ),
            "example_based": (
                "Ask the candidate to provide a specific example "
                "that supports the response."
            ),
            "deepening": (
                "Ask a deeper probing question that explores the "
                "candidate's response in greater detail."
            ),
            "scenario_based": (
                "Ask a scenario-based question that requires the "
                "candidate to apply the discussed experience or skill."
            ),
        }

        return {
            **decision,
            "instruction": instructions[follow_up_type],
        }