import numpy as np
import pytest

import scoring.semantic_matching as semantic_module


class FakeModel:
    def __init__(self, name):
        self.calls = []

    def encode(self, texts):
        self.calls.extend(texts)
        vectors = {
            "alpha": [1.0, 0.0],
            "beta": [0.0, 1.0],
            "gamma": [1.0, 1.0],
        }
        return np.array([vectors[text] for text in texts])


def make_matcher(monkeypatch, cache_size=512):
    monkeypatch.setattr(semantic_module, "SentenceTransformer", FakeModel)
    return semantic_module.SemanticMatching(cache_size=cache_size)


def test_repeated_text_uses_cached_embedding(monkeypatch):
    matcher = make_matcher(monkeypatch)
    first = matcher.similarity("alpha", "beta")
    second = matcher.similarity("alpha", "beta")

    assert first == second
    assert matcher.model.calls == ["alpha", "beta"]


def test_cache_respects_maximum_size(monkeypatch):
    matcher = make_matcher(monkeypatch, cache_size=2)
    matcher.similarity("alpha", "beta")
    matcher.similarity("gamma", "alpha")

    assert len(matcher._embedding_cache) == 2
    assert "beta" not in matcher._embedding_cache


def test_empty_text_returns_zero_without_encoding(monkeypatch):
    matcher = make_matcher(monkeypatch)

    assert matcher.similarity("", "alpha") == 0.0
    assert matcher.model.calls == []


def test_invalid_cache_size_is_rejected():
    with pytest.raises(ValueError):
        semantic_module.SemanticMatching(cache_size=0)


def test_compare_preserves_result_fields(monkeypatch):
    matcher = make_matcher(monkeypatch)
    result = matcher.compare(
        {"skills": "alpha", "experience": "beta", "projects": "gamma"},
        {"skills": "alpha", "experience": "beta", "projects": "gamma"},
    )

    assert result["overall_similarity"] == 100.0
    assert result["match_level"] == "Excellent Match"
    assert set(result) == {
        "skills_similarity",
        "experience_similarity",
        "project_similarity",
        "overall_similarity",
        "match_level",
    }
