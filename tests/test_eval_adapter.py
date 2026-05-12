import importlib
import json
import subprocess
import sys
from pathlib import Path

from eval_adapter.cli import load_config
from eval_adapter.runners import RUNNERS

ROOT = Path(__file__).resolve().parents[1]

def test_all_runners_normalize():
    config={"rubric":{"version":"auraone-rubric-v1","criteria":[{"criterion_id":"c1","weight":0.4},{"criterion_id":"c2","weight":0.6}]},"responses":[{"output_id":"out-1","labels":{"c1":0.5,"c2":1.0}}]}
    expected_scores = None
    for runner in RUNNERS:
        result=importlib.import_module(f"eval_adapter.runners.{runner}").run(config)
        assert result.item_count == 1
        assert [row["weighted_score"] for row in result.scores] == [0.2, 0.6]
        expected_scores = expected_scores or [(row["criterion_id"], row["score"], row["weight"]) for row in result.scores]
        assert [(row["criterion_id"], row["score"], row["weight"]) for row in result.scores] == expected_scores

def test_import_only_exports_normalize():
    exports = json.loads((ROOT / "examples/sample_exports.json").read_text())
    assert importlib.import_module("eval_adapter.runners.langsmith").import_results(exports["langsmith"]).scores[0]["criterion_id"] == "quality"
    assert importlib.import_module("eval_adapter.runners.phoenix").import_results(exports["phoenix"]).scores[0]["criterion_id"] == "quality"

def test_cli_runner_all():
    proc = subprocess.run(
        [sys.executable, "-m", "eval_adapter.cli", "run", "--config", str(ROOT / "examples/unified_config_sample.yaml"), "--runner", "all"],
        text=True,
        capture_output=True,
        env={"PYTHONPATH": str(ROOT / "src")},
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
    payload = json.loads(proc.stdout)
    assert set(payload) == set(RUNNERS)
    assert payload["inspect_ai"]["scores"][0]["criterion_id"] == "quality"


def test_load_config_accepts_real_yaml_and_json(tmp_path):
    yaml_config = load_config(ROOT / "examples/unified_config_sample.yaml")
    assert yaml_config["rubric"]["criteria"][0]["criterion_id"] == "quality"
    assert yaml_config["responses"][0]["labels"]["quality"] == 0.8

    json_path = tmp_path / "run.json"
    json_path.write_text(json.dumps(yaml_config), encoding="utf-8")
    assert load_config(json_path) == yaml_config
