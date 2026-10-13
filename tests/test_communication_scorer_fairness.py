from scoring.communication_scorer import CommunicationScorer


def test_empty_answer_returns_zero_score():
    result = CommunicationScorer().evaluate("")

    assert result["communication_score"] == 0.0
    assert all(
        score == 0.0
        for score in result["component_scores"].values()
    )


def test_whitespace_answer_returns_zero_score():
    result = CommunicationScorer().evaluate("   ")

    assert result["communication_score"] == 0.0


def test_all_scores_stay_within_zero_and_one_hundred():
    scorer = CommunicationScorer()

    answers = [
        "Yes.",
        "I completed a project.",
        (
            "I worked on a data analysis project. "
            "I cleaned the data and checked for missing values. "
            "Then I created visualizations and explained the results."
        ),
        " ".join(["I analyzed the data carefully."] * 30),
    ]

    for answer in answers:
        result = scorer.evaluate(answer)

        assert 0.0 <= result["communication_score"] <= 100.0
        assert all(
            0.0 <= score <= 100.0
            for score in result["component_scores"].values()
        )


def test_component_weights_total_one_hundred():
    assert sum(CommunicationScorer.WEIGHTS.values()) == 100


def test_component_scores_and_output_keys_remain_available():
    result = CommunicationScorer().evaluate(
        "I analyzed customer data and presented the findings."
    )

    assert set(result["component_scores"]) == {
        "fluency",
        "grammar_quality",
        "vocabulary_range",
        "clarity",
        "filler_words",
        "answer_structure",
    }
    assert "filler_word_analysis" in result
    assert "statistics" in result


def test_fluency_is_not_penalized_for_sentence_length():
    scorer = CommunicationScorer()

    short_sentences = "I worked. I learned. I improved."
    long_sentence = (
        "I worked on a project where I analyzed the available data, "
        "cleaned the dataset, developed visualizations, and presented "
        "the findings to explain the results."
    )

    short_result = scorer.evaluate(short_sentences)
    long_result = scorer.evaluate(long_sentence)

    assert (
        short_result["component_scores"]["fluency"]
        == long_result["component_scores"]["fluency"]
    )


def test_vocabulary_score_does_not_depend_on_word_variety():
    scorer = CommunicationScorer()

    repetitive = "data data data data data data"
    varied = "data analysis reports charts insights findings"

    repetitive_result = scorer.evaluate(repetitive)
    varied_result = scorer.evaluate(varied)

    assert (
        repetitive_result["component_scores"]["vocabulary_range"]
        == varied_result["component_scores"]["vocabulary_range"]
    )
