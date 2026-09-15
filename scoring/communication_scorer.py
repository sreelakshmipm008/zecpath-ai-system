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
        "fluency": 20,
        "grammar_quality": 20,
        "vocabulary_range": 15,
        "clarity": 20,
        "filler_words": 10,
        "answer_structure": 15,
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
        """
        Measure sentence continuity.

        The score considers:
        - reasonable sentence length
        - sentence completeness
        - excessive fragmentation
        - answer continuity

        The result is normalized to 0-100.
        """

        if word_count == 0:
            return 0.0

        if sentence_count == 0:
            return 0.0

        average_sentence_length = word_count / sentence_count

        # Reasonable conversational sentence length.
        if 8 <= average_sentence_length <= 22:
            length_score = 100
        elif 5 <= average_sentence_length < 8:
            length_score = 80
        elif 22 < average_sentence_length <= 30:
            length_score = 80
        elif 3 <= average_sentence_length < 5:
            length_score = 60
        else:
            length_score = 45

        # Penalize very short fragmented sentences.
        short_sentences = sum(
            1 for sentence in sentences
            if len(self._tokenize_words(sentence)) < 3
        )

        fragmentation_rate = short_sentences / sentence_count

        fragmentation_penalty = min(
            30,
            fragmentation_rate * 60
        )

        score = length_score - fragmentation_penalty

        return round(self._clamp(score), 2)

    # ---------------------------------------------------------
    # 2. Grammar Quality
    # ---------------------------------------------------------

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
        """
        Measure vocabulary range using lexical diversity.

        Type-token ratio is calculated using a minimum analysis
        window to reduce bias from very short/long answers.
        """

        if word_count == 0:
            return 0.0

        unique_words = len(set(words))

        # Use a bounded word count so answer length does not
        # dominate the score.
        analysis_count = min(word_count, 100)

        bounded_words = words[:analysis_count]

        unique_bounded_words = len(set(bounded_words))

        lexical_diversity = (
            unique_bounded_words / analysis_count
        )

        # Normalize typical conversational lexical diversity.
        score = ((lexical_diversity - 0.20) / 0.60) * 100

        return round(self._clamp(score), 2)

    # ---------------------------------------------------------
    # 4. Clarity of Explanation
    # ---------------------------------------------------------

    def _clarity_score(
        self,
        words: List[str],
        sentences: List[str],
        word_count: int,
        sentence_count: int
    ) -> float:
        """
        Measure clarity using:
        - reasonable sentence length
        - sufficient explanation
        - excessive sentence complexity penalty
        """

        if word_count == 0:
            return 0.0

        if sentence_count == 0:
            return 0.0

        average_sentence_length = word_count / sentence_count

        if 8 <= average_sentence_length <= 20:
            sentence_score = 100
        elif 5 <= average_sentence_length < 8:
            sentence_score = 80
        elif 20 < average_sentence_length <= 28:
            sentence_score = 80
        elif average_sentence_length > 28:
            sentence_score = 60
        else:
            sentence_score = 55

        # Explanation depth.
        if word_count >= 80:
            explanation_score = 100
        elif word_count >= 50:
            explanation_score = 90
        elif word_count >= 25:
            explanation_score = 75
        elif word_count >= 10:
            explanation_score = 60
        else:
            explanation_score = 45

        score = (
            sentence_score * 0.60
            + explanation_score * 0.40
        )

        return round(self._clamp(score), 2)

    # ---------------------------------------------------------
    # 5. Filler Words
    # ---------------------------------------------------------

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

        # Lower filler rate = better communication.
        if filler_rate <= 1:
            score = 100
        elif filler_rate <= 2:
            score = 90
        elif filler_rate <= 4:
            score = 75
        elif filler_rate <= 6:
            score = 60
        elif filler_rate <= 8:
            score = 45
        else:
            score = 30

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
        """
        Measure organization and logical answer structure.

        Structure indicators include:
        - multiple sentences
        - logical transition markers
        - explanation length
        """

        if word_count == 0:
            return 0.0

        score = 45.0

        if len(sentences) >= 2:
            score += 20

        if len(sentences) >= 4:
            score += 10

        marker_count = 0

        for marker in self.STRUCTURE_MARKERS:
            if re.search(
                r"\b" + re.escape(marker) + r"\b",
                text
            ):
                marker_count += 1

        score += min(marker_count * 5, 20)

        if word_count >= 25:
            score += 5

        return round(self._clamp(score), 2)

    # ---------------------------------------------------------
    # Final Score
    # ---------------------------------------------------------

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