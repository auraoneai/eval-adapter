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
    scores = _extract_scores(raw)
    item_count = raw.get("item_count")
    if item_count is None:
        output_ids = {row.get("output_id") for row in scores if row.get("output_id") is not None}
        item_count = len(output_ids) if output_ids else len(scores)
    metadata = {"source": runner, "synthetic": raw.get("synthetic", True), **raw.get("metadata", {})}
    return EvalRunResult(runner, int(item_count), scores, metadata)


def _extract_scores(raw: dict[str, Any]) -> list[dict[str, Any]]:
    if "scores" in raw:
        return list(raw["scores"])
    if "results" in raw:
        return list(raw["results"])
    if "evaluations" in raw:
        return list(raw["evaluations"])
    if "feedback" in raw:
        return [
            {
                "output_id": row.get("run_id", row.get("output_id")),
                "criterion_id": row.get("key", row.get("criterion_id")),
                "score": row.get("score"),
                "weight": row.get("weight", 1.0),
            }
            for row in raw["feedback"]
        ]
    if "traces" in raw:
        return [
            {
                "output_id": trace.get("trace_id", trace.get("output_id")),
                "criterion_id": trace.get("metric", trace.get("criterion_id")),
                "score": trace.get("score"),
                "weight": trace.get("weight", 1.0),
            }
            for trace in raw["traces"]
        ]
    return []
