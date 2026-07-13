from __future__ import annotations

import json
from pathlib import Path
from typing import Any


TARGETS = ("lm-eval-harness", "inspect", "openai-evals", "promptfoo")


def load_rubric(path: str | Path) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or not isinstance(payload.get("criteria"), list):
        raise ValueError("rubric must be a rubric-spec JSON object with criteria")
    return payload


def export_rubric(rubric_path: str | Path, target: str, out: str | Path) -> list[Path]:
    if target not in TARGETS:
        raise ValueError(f"unsupported target: {target}")
    rubric = load_rubric(rubric_path)
    output = Path(out)
    output.mkdir(parents=True, exist_ok=True)
    files = _files_for_target(rubric, target)
    written = []
    for name, text in files.items():
        path = output / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        written.append(path)
    return written


def _files_for_target(rubric: dict[str, Any], target: str) -> dict[str, str]:
    if target == "lm-eval-harness":
        return {"auraone_rubric_task.yaml": _lm_eval(rubric), "rubric.json": _json(rubric)}
    if target == "inspect":
        return {"task.py": _inspect(rubric), "rubric.json": _json(rubric)}
    if target == "openai-evals":
        return {"eval.yaml": _openai_evals(rubric), "rubric.json": _json(rubric)}
    return {"promptfooconfig.yaml": _promptfoo(rubric), "rubric.json": _json(rubric)}


def _json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def _ids(rubric: dict[str, Any]) -> list[str]:
    return [str(criterion["criterion_id"]) for criterion in rubric.get("criteria", [])]


def _lm_eval(rubric: dict[str, Any]) -> str:
    return f"""task: auraone_{rubric.get('rubric_id', 'rubric')}
dataset_path: json
metric_list:
  - metric: auraone_rubric_score
metadata:
  rubric_spec: auraone-rubric-v1
  criteria: {json.dumps(_ids(rubric))}
"""


def _inspect(rubric: dict[str, Any]) -> str:
    return f'''from inspect_ai import Task

RUBRIC_ID = "{rubric.get("rubric_id", "rubric")}"
CRITERIA = {json.dumps(rubric.get("criteria", []), indent=2, sort_keys=True)}


def task():
    return Task(dataset=[], scorer=[])
'''


def _openai_evals(rubric: dict[str, Any]) -> str:
    return f"""evals:
  {rubric.get('rubric_id', 'auraone_rubric')}:
    class: evals.elsuite.basic.match:Match
    args:
      rubric_spec: rubric.json
"""


def _promptfoo(rubric: dict[str, Any]) -> str:
    checks = "\n".join(f"      - type: javascript\n        value: output => true # {criterion_id}" for criterion_id in _ids(rubric))
    return f"""description: AuraOne rubric export for {rubric.get('rubric_id', 'rubric')}
providers: []
prompts: []
tests:
  - assert:
{checks}
"""
