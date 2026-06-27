from __future__ import annotations


class SafetyFilterService:
    def sanitize(self, text: str) -> str:
        return text.strip()
