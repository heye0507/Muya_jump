import pytest

from src.jump_classification.classifier import classify_jump


def test_jump_classification_is_reserved_for_phase_two():
    with pytest.raises(NotImplementedError, match="Phase 2"):
        classify_jump([])
