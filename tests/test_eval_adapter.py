from eval_adapter.runners import RUNNERS
import importlib

def test_all_runners_normalize():
    config={"rubric":{"criteria":[{"criterion_id":"c1","weight":1.0}]}}
    for runner in RUNNERS:
        result=importlib.import_module(f"eval_adapter.runners.{runner}").run(config)
        assert result.item_count == 1
