# Runner Coverage Matrix

`eval-adapter` normalizes local configuration and export-shaped data. It does not import, install, invoke, or verify the external frameworks named below.

| Runner module | Synthetic config normalization | Export-shaped import helper | Rubric export scaffold |
| --- | --- | --- | --- |
| Inspect AI | yes | yes | yes |
| LM Eval Harness | yes | yes | yes |
| OpenAI Evals | yes | yes | yes |
| PromptFoo | yes | yes | yes |
| DeepEval | yes | yes | no |
| LangSmith | yes | feedback rows | no |
| Phoenix | yes | trace rows | no |

All runner modules emit `runner`, `item_count`, `scores`, and `metadata`. Per-score rows preserve `output_id`, `criterion_id`, raw `score`, `weight`, `weighted_score`, and a `runner_native_key`.

The four export targets produce starter files, not runnable evaluations:

- LM Eval Harness: task YAML plus `rubric.json`.
- Inspect AI: `task.py` scaffold plus `rubric.json`.
- OpenAI Evals: eval YAML plus `rubric.json`.
- PromptFoo: config YAML with placeholder JavaScript assertions plus `rubric.json`.

Before using an export, add the target framework's dataset, provider, scorer, and execution configuration, then test it with that framework's own validation and runtime.
