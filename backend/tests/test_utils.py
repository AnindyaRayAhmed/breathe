from __future__ import annotations

from backend.utils.validators import clean_text, has_meaningful_text


def test_clean_text_normalizes_spacing() -> None:
    assert clean_text("  breathe   well  ") == "breathe well"


def test_has_meaningful_text_detects_content() -> None:
    assert has_meaningful_text("  reflection  ") is True
    assert has_meaningful_text("   ") is False

