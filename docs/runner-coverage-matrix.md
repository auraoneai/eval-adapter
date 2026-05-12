# Runner Coverage Matrix

| Runner | Run | Import | Rubric weights | Drift |
| --- | --- | --- | --- | --- |
| Inspect AI | yes | yes | yes | planned |
| LM Eval Harness | yes | yes | yes | planned |
| OpenAI Evals | yes | yes | yes | planned |
| PromptFoo | yes | yes | yes | planned |
| DeepEval | yes | yes | yes | planned |
| LangSmith | synthetic normalization + import | yes | yes | planned |
| Phoenix | synthetic normalization + import | yes | yes | planned |

All runners emit the same canonical fields: `runner`, `item_count`, `scores`, and
`metadata`. Per-score rows preserve `output_id`, `criterion_id`, raw `score`,
`weight`, normalized `weighted_score`, and a `runner_native_key` that identifies the
framework-specific mapping used during normalization.
