from __future__ import annotations

import argparse
import importlib
import json
from pathlib import Path
from typing import Any

import yaml

from .runners import RUNNERS
from .exporters import TARGETS, export_rubric


def load_config(path: str | Path) -> dict[str, Any]:
    config_path = Path(path)
    text = config_path.read_text(encoding="utf-8")
    parsed = json.loads(text) if config_path.suffix.lower() == ".json" else yaml.safe_load(text)
    if not isinstance(parsed, dict):
        raise ValueError("config file must parse to a mapping")
    return parsed


def main(argv=None):
    p=argparse.ArgumentParser(prog="eval-adapter"); sub=p.add_subparsers(dest="cmd", required=True)
    r=sub.add_parser("run"); r.add_argument("--config", required=True); r.add_argument("--runner", required=True, choices=RUNNERS+["all"])
    e=sub.add_parser("export"); e.add_argument("--rubric", required=True); e.add_argument("--to", required=True, choices=TARGETS); e.add_argument("--out", required=True)
    args=p.parse_args(argv)
    if args.cmd == "export":
        paths = export_rubric(args.rubric, args.to, args.out)
        print(json.dumps({"ok": True, "target": args.to, "paths": [str(path) for path in paths]}, indent=2))
        return 0
    config=load_config(args.config)
    runners=RUNNERS if args.runner == "all" else [args.runner]
    out={name: importlib.import_module(f"eval_adapter.runners.{name}").run(config).to_dict() for name in runners}
    print(json.dumps(out, indent=2)); return 0
if __name__ == "__main__": raise SystemExit(main())
