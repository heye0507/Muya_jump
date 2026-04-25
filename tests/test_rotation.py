import pytest

from src.rotation_counter.counter import count_rotation


def test_rotation_counting_is_reserved_for_phase_two():
    with pytest.raises(NotImplementedError, match="Phase 2"):
        count_rotation([])
