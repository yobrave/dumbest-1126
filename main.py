# Dumbest Agent Moment entry shipper: single 200-char line in, receipt out.

import json
import os
import re
from pathlib import Path

LIMIT = 200
FLOOR = 1
STAMP = "dmb-11260042"


def ship():
    origin = Path(__file__).resolve().parent / "entry.txt"
    raw = origin.read_text(encoding="utf-8")
    line = re.sub(r"\s+", " ", raw).strip()
    if (n := len(line)) < 1:
        raise SystemExit(json.dumps({"gate_pass": False, "artifact": None, "note": "blank"}))
    if n > LIMIT:
        raise SystemExit(json.dumps({"gate_pass": False, "artifact": None, "note": f"{n} chars"}))
    dest = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "out")
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "entry.txt").write_text(line + "\n", encoding="utf-8", newline="\n")
    if not (dest / "entry.txt").exists():
        raise SystemExit(json.dumps({"gate_pass": False, "note": "copy missing"}))
    print(json.dumps({"gate_pass": True, "artifact": str(dest / "entry.txt"), "chars": n, "stamp": STAMP}))


if __name__ == "__main__":
    ship()
