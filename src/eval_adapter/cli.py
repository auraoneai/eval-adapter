from __future__ import annotations
import argparse, importlib, json
from pathlib import Path
from .runners import RUNNERS

def main(argv=None):
    p=argparse.ArgumentParser(prog="eval-adapter"); sub=p.add_subparsers(dest="cmd", required=True)
    r=sub.add_parser("run"); r.add_argument("--config", required=True); r.add_argument("--runner", required=True, choices=RUNNERS+["all"])
    args=p.parse_args(argv); config=json.loads(Path(args.config).read_text())
    runners=RUNNERS if args.runner == "all" else [args.runner]
    out={name: importlib.import_module(f"eval_adapter.runners.{name}").run(config).to_dict() for name in runners}
    print(json.dumps(out, indent=2)); return 0
if __name__ == "__main__": raise SystemExit(main())
