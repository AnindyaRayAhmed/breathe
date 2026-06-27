from __future__ import annotations


def clean_text(value: str) -> str:
    return " ".join(value.strip().split())


def has_meaningful_text(value: str) -> bool:
    return len(clean_text(value)) > 0

