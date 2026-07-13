# eval-adapter

Export `rubric-spec` rubrics and normalize evaluation result shapes across common eval frameworks.

`eval-adapter` is for evaluation infrastructure engineers migrating rubric and result contracts between tools. Its differentiator is one inspectable `EvalRunResult` shape with `output_id`, `criterion_id`, raw score, weight, weighted score, runner identity, and source metadata.

## What It Actually Adapts

- `run` creates deterministic synthetic normalized results for the bundled Inspect AI, LM Eval Harness, OpenAI Evals, PromptFoo, DeepEval, LangSmith, and Phoenix runner modules.
- LangSmith feedback exports and Phoenix trace exports can be normalized through their Python import helpers.
- `export` writes starter rubric files for LM Eval Harness, Inspect AI, OpenAI Evals, or PromptFoo.

The package does not import or execute those frameworks. Generated files are scaffolds that require framework-specific datasets, scorers, providers, and review before production use.

## Inspectable Output

`eval-adapter run` writes canonical JSON to stdout. `eval-adapter export` writes a target-specific YAML or Python starter file plus the original `rubric.json`, then reports every written path as JSON.

## Runtime Boundary

All operations are local file parsing, deterministic normalization, and file generation. Runtime dependencies are `PyYAML` and `rubric-spec`. There are no network requests, model calls, provider credentials, or hosted state.

## Install

```bash
python -m pip install eval-adapter==0.1.2
```

For development from a clone:

```bash
python -m pip install -e .
```

## Quickstart

From a repository checkout:

```bash
eval-adapter run \
  --config examples/unified_config_sample.yaml \
  --runner all \
  > normalized-results.json
```

## Documentation

- Coverage and capability boundaries: [`docs/runner-coverage-matrix.md`](docs/runner-coverage-matrix.md)
- Migration guides: [`docs/`](docs/)
- Import-shaped examples: [`examples/sample_exports.json`](examples/sample_exports.json)

## Release Status

Registry status verified July 13, 2026: version `0.1.2` is published on PyPI and tagged `v0.1.2` in the public repository. The project is alpha software. No framework partnership, production-compatibility, or adoption claim is made.

## Limits

Normalized synthetic results and generated starter files are not evidence that an external framework ran successfully. This is not a hosted evaluation platform and includes no customer data.

## Next Action

Run the sample config with `--runner all`, verify criterion ids and weights in one normalized result, then export only the intended target and validate that scaffold with the target framework's own tooling.
