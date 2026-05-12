from __future__ import annotations
from eval_adapter.results.canonical import normalize

def run(config: dict):
    criteria = config.get("rubric", {}).get("criteria", [])
    scores = [{"criterion_id": c.get("criterion_id"), "score": 1.0, "weight": c.get("weight", 1.0)} for c in criteria]
    return normalize(__name__.split(".")[-1], {"scores": scores, "synthetic": True})

def import_results(export: dict):
    return normalize(__name__.split(".")[-1], export)
