from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class RunConfig:
    rubric: dict[str, Any]
    responses_source: str
    judge_config: dict[str, Any] = field(default_factory=dict)
    sampling: dict[str, Any] = field(default_factory=lambda: {"limit": None})
    reporting: dict[str, Any] = field(default_factory=lambda: {"format": "json"})
