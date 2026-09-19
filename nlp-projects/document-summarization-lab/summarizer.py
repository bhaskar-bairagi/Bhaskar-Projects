"""Reproducible extractive summarization baselines and simple diagnostics."""
from __future__ import annotations

import re
from collections import Counter

STOP = {"a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "in", "is",
        "it", "of", "on", "or", "that", "the", "to", "was", "were", "with"}


def sentences(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+", text.strip()) if part.strip()]


def words(text: str) -> list[str]:
    return [word for word in re.findall(r"[a-z0-9]+", text.lower()) if word not in STOP]


def summarize(text: str, method: str = "frequency", count: int = 2) -> str:
    items = sentences(text)
    if not items or count < 1:
        raise ValueError("Provide text and a positive sentence count")
    count = min(count, len(items))
    if method == "lead":
        indexes = list(range(count))
    elif method == "frequency":
        frequencies = Counter(words(text))
        scored = [(sum(frequencies[word] for word in set(words(sentence))) / max(len(words(sentence)), 1),
                   -index, index) for index, sentence in enumerate(items)]
        indexes = sorted(row[2] for row in sorted(scored, reverse=True)[:count])
    else:
        raise ValueError("Unknown method")
    return " ".join(items[index] for index in indexes)


def evaluate(source: str, summary: str, key_terms: list[str]) -> dict[str, float | bool]:
    """Diagnostics, not a claim of semantic quality or factual correctness."""
    original = sentences(source)
    selected = sentences(summary)
    supported = all(sentence in original for sentence in selected)
    normalized = summary.lower()
    terms = [term.strip().lower() for term in key_terms if term.strip()]
    coverage = sum(term in normalized for term in terms) / len(terms) if terms else 0.0
    compression = len(words(summary)) / len(words(source)) if words(source) else 0.0
    return {"source_sentence_support": supported,
            "key_term_coverage": round(coverage, 3), "word_ratio": round(compression, 3)}
