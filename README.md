# eval-adapter

`eval-adapter` lets one rubric-spec v1 rubric and run config drive synthetic-compatible runs across Inspect AI, LM Eval Harness, OpenAI Evals, PromptFoo, DeepEval, LangSmith exports, and Phoenix exports.

## Quickstart

```bash
pip install eval-adapter
eval-adapter run --config examples/unified_config_sample.yaml --runner all
```

The runner modules normalize each framework shape into one `EvalRunResult` containing
`item_count`, per-criterion scores, weights, weighted scores, and source metadata.
LangSmith and Phoenix exports can be imported from their feedback/trace shapes; see
`examples/sample_exports.json`.

## What This Is Not

This is not a hosted eval platform and includes no paid or customer data.
