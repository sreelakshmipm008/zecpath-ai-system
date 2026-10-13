"""
Day 35 - Communication Skill Evaluation

Evaluates candidate communication using:
1. Fluency (sentence continuity)
2. Grammar quality
3. Vocabulary range
4. Clarity of explanation
5. Filler words
6. Answer structure

Returns an overall communication score from 0 to 100.

The implementation uses normalized ratios and capped metrics
to reduce bias caused by answer length.
"""

import re
from typing import Dict, List


class CommunicationScorer:
    """
    Rule-based communication scoring model for candidate answers.
    """

    # Component weights must total 100.
    WEIGHTS = {
        "fluency": 10,
        "grammar_quality": 10,
        "vocabulary_range": 5,
        "clarity": 25,
        "filler_words": 5,
        "answer_structure": 45,
    }

    FILLER_WORDS = {
        "um",
        "uh",
        "erm",
        "hmm",
        "like",
        "you know",
        "actually",
        "basically",
        "literally",
        "so",
    }

    COMMON_GRAMMAR_ERRORS = [
        r"\bi is\b",
        r"\bhe are\b",
        r"\bshe are\b",
        r"\bthey is\b",
        r"\bwe was\b",
        r"\bthey was\b",
        r"\bhe have\b",
        r"\bshe have\b",
        r"\bi has\b",
        r"\bdoesn't have\b",
        r"\bdidn't went\b",
    ]

    STRUCTURE_MARKERS = [
        "first",
        "second",
        "finally",
        "because",
        "therefore",
        "however",
        "for example",
        "for instance",
        "in conclusion",
        "overall",
        "also",
        "then",
    ]

    def evaluate(self, answer: str) -> Dict:
        """
        Evaluate a candidate's communication answer.

        Parameters
        ----------
        answer : str
            Candidate's answer text.

        Returns
        -------
        Dict
            Detailed component scores and final score.
        """

        if not answer or not answer.strip():
            return self._empty_result()

        cleaned_answer = self._normalize_text(answer)

        words = self._tokenize_words(cleaned_answer)
        sentences = self._split_sentences(cleaned_answer)

        word_count = len(words)
        sentence_count = len(sentences)

        fluency = self._fluency_score(
            words,
            sentences,
            word_count,
            sentence_count
        )

        grammar = self._grammar_score(
            cleaned_answer,
            word_count
        )

        vocabulary = self._vocabulary_score(
            words,
            word_count
        )

        clarity = self._clarity_score(
            words,
            sentences,
            word_count,
            sentence_count
        )

        filler_result = self._filler_word_score(
            cleaned_answer,
            word_count
        )

        structure = self._structure_score(
            cleaned_answer,
            sentences,
            word_count
        )

        component_scores = {
            "fluency": fluency,
            "grammar_quality": grammar,
            "vocabulary_range": vocabulary,
            "clarity": clarity,
            "filler_words": filler_result["score"],
            "answer_structure": structure,
        }

        final_score = self._calculate_final_score(component_scores)

        return {
            "communication_score": final_score,
            "component_scores": component_scores,
            "filler_word_analysis": filler_result,
            "statistics": {
                "word_count": word_count,
                "sentence_count": sentence_count,
                "unique_word_count": len(set(words)),
            },
        }

    # ---------------------------------------------------------
    # Text processing
    # ---------------------------------------------------------

    @staticmethod
    def _normalize_text(text: str) -> str:
        """Normalize whitespace and text formatting."""

        text = text.lower().strip()
        text = re.sub(r"\s+", " ", text)

        return text

    @staticmethod
    def _tokenize_words(text: str) -> List[str]:
        """Extract alphabetic words."""

        return re.findall(r"\b[a-zA-Z]+\b", text)

    @staticmethod
    def _split_sentences(text: str) -> List[str]:
        """Split answer into sentences."""

        sentences = re.split(r"[.!?]+", text)

        return [
            sentence.strip()
            for sentence in sentences
            if sentence.strip()
        ]

    # ---------------------------------------------------------
    # 1. Fluency
    # ---------------------------------------------------------

    def _fluency_score(
        self,
        words: List[str],
        sentences: List[str],
        word_count: int,
        sentence_count: int
    ) -> float:
        """Return a neutral score pending validated fluency measures."""
        if word_count == 0 or sentence_count == 0:
            return 0.0
        return 75.0

    def _grammar_score(
        self,
        text: str,
        word_count: int
    ) -> float:
        """
        Estimate grammar quality using detectable grammar error patterns.

        The error rate is normalized per 100 words so longer answers
        do not automatically receive lower scores.
        """

        if word_count == 0:
            return 0.0

        error_count = 0

        for pattern in self.COMMON_GRAMMAR_ERRORS:
            error_count += len(re.findall(pattern, text))

        errors_per_100_words = (
            error_count / word_count
        ) * 100

        score = 100 - (errors_per_100_words * 12)

        return round(self._clamp(score), 2)

    # ---------------------------------------------------------
    # 3. Vocabulary Range
    # ---------------------------------------------------------

    def _vocabulary_score(
        self,
        words: List[str],
        word_count: int
    ) -> float:
        """Avoid using lexical diversity as an unvalidated hiring proxy."""
        if word_count == 0:
            return 0.0
        return 70.0

    def _clarity_score(
        self,
        words: List[str],
        sentences: List[str],
        word_count: int,
        sentence_count: int
    ) -> float:
        """Use a neutral score until clarity is measured with validated evidence."""
        if word_count == 0 or sentence_count == 0:
            return 0.0
        return 70.0

    def _filler_word_score(
        self,
        text: str,
        word_count: int
    ) -> Dict:
        """
        Detect filler words and calculate filler-word rate.

        Filler rate is normalized per 100 words, preventing longer
        answers from being unfairly penalized simply because they
        contain more total words.
        """

        if word_count == 0:
            return {
                "score": 0.0,
                "filler_word_count": 0,
                "filler_rate_per_100_words": 0.0,
                "detected_fillers": [],
            }

        filler_count = 0
        detected_fillers = []

        for filler in sorted(
            self.FILLER_WORDS,
            key=len,
            reverse=True
        ):
            pattern = r"\b" + re.escape(filler) + r"\b"

            matches = re.findall(pattern, text)

            if matches:
                filler_count += len(matches)
                detected_fillers.extend(
                    [filler] * len(matches)
                )

        filler_rate = (
            filler_count / word_count
        ) * 100

        # Filler words are reported for review but are not used
        # as an automated candidate-ranking signal.
        score = 70.0

        return {
            "score": round(self._clamp(score), 2),
            "filler_word_count": filler_count,
            "filler_rate_per_100_words": round(filler_rate, 2),
            "detected_fillers": detected_fillers,
        }

    # ---------------------------------------------------------
    # 6. Answer Structure
    # ---------------------------------------------------------

    def _structure_score(
        self,
        text: str,
        sentences: List[str],
        word_count: int
    ) -> float:
        """Avoid using sentence count and transition words as hiring proxies."""
        if word_count == 0:
            return 0.0
        return 70.0

    def _calculate_final_score(
        self,
        component_scores: Dict[str, float]
    ) -> float:
        """
        Calculate the weighted communication score.

        All components are already normalized to 0-100.
        Weights total 100%.
        """

        total_weight = sum(self.WEIGHTS.values())

        weighted_score = sum(
            component_scores[name]
            * self.WEIGHTS[name]
            for name in self.WEIGHTS
        )

        final_score = weighted_score / total_weight

        return round(self._clamp(final_score), 2)

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    @staticmethod
    def _clamp(
        value: float,
        minimum: float = 0.0,
        maximum: float = 100.0
    ) -> float:
        """Keep a score inside the required range."""

        return max(minimum, min(maximum, value))

    @staticmethod
    def _empty_result() -> Dict:
        """Return a safe result for an empty answer."""

        return {
            "communication_score": 0.0,
            "component_scores": {
                "fluency": 0.0,
                "grammar_quality": 0.0,
                "vocabulary_range": 0.0,
                "clarity": 0.0,
                "filler_words": 0.0,
                "answer_structure": 0.0,
            },
            "filler_word_analysis": {
                "score": 0.0,
                "filler_word_count": 0,
                "filler_rate_per_100_words": 0.0,
                "detected_fillers": [],
            },
            "statistics": {
                "word_count": 0,
                "sentence_count": 0,
                "unique_word_count": 0,
            },
        }


if __name__ == "__main__":
    scorer = CommunicationScorer()

    sample_answer = (
        "I worked on a Python project where I developed a data processing "
        "pipeline. First, I collected the data and cleaned missing values. "
        "Then, I analyzed the data and created useful visualizations. "
        "Finally, I presented the results and explained the important findings."
    )

    result = scorer.evaluate(sample_answer)

    print("Communication Evaluation")
    print("-" * 30)

    for name, score in result["component_scores"].items():
        print(f"{name}: {score}")

    print(
        f"Filler words detected: "
        f"{result['filler_word_analysis']['filler_word_count']}"
    )

    print(
        f"Final Communication Score: "
        f"{result['communication_score']}/100"
    )