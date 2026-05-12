from __future__ import annotations

from typing import Any

from eval_adapter.results.canonical import normalize


def run_config(runner: str, config: dict[str, Any], framework: str) -> Any:
    criteria = _criteria(config)
    responses = _responses(config)
    scores = []
    for index, response in enumerate(responses, start=1):
        output_id = str(response.get("output_id") or response.get("id") or f"item-{index}")
        labels = response.get("labels", {})
        default_score = float(response.get("score", 1.0))
        for criterion in criteria:
            criterion_id = str(criterion["criterion_id"])
            score = float(labels.get(criterion_id, default_score))
            weight = float(criterion.get("weight", 1.0))
            scores.append(
                {
                    "output_id": output_id,
                    "criterion_id": criterion_id,
                    "score": score,
                    "weight": weight,
                    "weighted_score": round(score * weight, 6),
                    "runner_native_key": f"{framework}:{criterion_id}",
                }
            )
    return normalize(
        runner,
        {
            "scores": scores,
            "item_count": len(responses),
            "synthetic": True,
            "metadata": {"framework": framework, "rubric_version": config.get("rubric", {}).get("version")},
        },
    )


def import_export(runner: str, export: dict[str, Any], framework: str) -> Any:
    result = normalize(runner, {**export, "metadata": {"framework": framework, **export.get("metadata", {})}})
    return result


def _criteria(config: dict[str, Any]) -> list[dict[str, Any]]:
    criteria = config.get("rubric", {}).get("criteria", [])
    if not criteria:
        raise ValueError("config.rubric.criteria must contain at least one criterion")
    for criterion in criteria:
        if not criterion.get("criterion_id"):
            raise ValueError("each rubric criterion needs criterion_id")
    return list(criteria)


def _responses(config: dict[str, Any]) -> list[dict[str, Any]]:
    responses = config.get("responses")
    if responses is None:
        responses = [{"output_id": "synthetic-1", "score": 1.0}]
    if not responses:
        raise ValueError("config.responses must contain at least one response when supplied")
    return list(responses)
