"""Jump type classification entry points."""

from typing import Any, Dict, Sequence


def classify_jump(frames: Sequence[Any]) -> Dict[str, Any]:
    """Classify a jump type from key frames.

    Phase 2 will replace this placeholder with observation-driven logic.
    """
    raise NotImplementedError("Phase 2 will implement jump type classification.")
