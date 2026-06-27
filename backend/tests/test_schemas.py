from __future__ import annotations

import pytest
from pydantic import ValidationError

from backend.schemas.onboarding import OnboardingRequest


def test_onboarding_schema_validation() -> None:
    with pytest.raises(ValidationError):
        OnboardingRequest(active_exams=[], primary_stressor_exam="")
