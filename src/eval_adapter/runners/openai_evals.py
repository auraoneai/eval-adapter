from __future__ import annotations
from eval_adapter.runners.common import import_export, run_config

def run(config: dict):
    return run_config(__name__.split(".")[-1], config, "openai_evals")

def import_results(export: dict):
    return import_export(__name__.split(".")[-1], export, "openai_evals")
