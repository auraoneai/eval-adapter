# eval-adapter

`eval-adapter` lets one rubric-spec v1 rubric and run config drive synthetic-compatible runs across Inspect AI, LM Eval Harness, OpenAI Evals, PromptFoo, DeepEval, LangSmith exports, and Phoenix exports.

## Quickstart

```bash
pip install eval-adapter
python -m json.tool examples/unified_config_sample.yaml > /tmp/run.json
eval-adapter run --config /tmp/run.json --runner all
```

## What This Is Not

This is not a hosted eval platform and includes no paid or customer data.
