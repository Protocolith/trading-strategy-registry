"""Check every evaluation record: valid JSON, required fields, catalog id pattern, matching spec, hash listed on the ledger.

    python3 tools/check_records.py

Stdlib only. Exit 1 with a list of problems, 0 when every record is consistent.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ID = re.compile(r"^MN-[A-Z]{2,5}-[A-Z]{2,5}-[0-9]{3}$")
REQUIRED = ("schema_version", "catalog_id", "visibility", "taxonomy", "protocol", "evaluation")


def main() -> int:
    ledger = (ROOT / "ledger" / "ledger.jsonl").read_text(encoding="utf-8")
    problems: list[str] = []
    records = sorted((ROOT / "records").glob("*.json"))
    for path in records:
        rec = json.loads(path.read_text(encoding="utf-8"))
        cid = rec.get("catalog_id", "")
        problems += [f"{path.name}: missing {k}" for k in REQUIRED if k not in rec]
        if rec.get("schema_version") != "strategy-evaluation/1":
            problems.append(f"{path.name}: schema_version is not strategy-evaluation/1")
        if not ID.match(cid) or path.stem != cid:
            problems.append(f"{path.name}: catalog id {cid!r} is malformed or does not match the file name")
        if rec.get("visibility") == "public" and not (ROOT / "specs" / f"{cid}.spec.json").exists():
            problems.append(f"{path.name}: public record without specs/{cid}.spec.json")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest not in ledger:
            problems.append(f"{path.name}: sha256 {digest[:12]} is not referenced by any ledger record")
    for p in problems:
        print(p)
    print(f"{len(records)} records, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
