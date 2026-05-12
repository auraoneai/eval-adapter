from __future__ import annotations
from dataclasses import dataclass
from typing import Any
@dataclass(frozen=True)
class EvalRunResult:
    runner: str
    item_count: int
    scores: list[dict[str, Any]]
    metadata: dict[str, Any]
    def to_dict(self): return self.__dict__
def normalize(runner: str, raw: dict[str, Any]) -> EvalRunResult:
    scores = raw.get("scores", raw.get("results", []))
    return EvalRunResult(runner, len(scores), list(scores), {"source": runner, "synthetic": raw.get("synthetic", True)})
